from __future__ import annotations

import json
import re
import time
import urllib.error
import urllib.request
from typing import Protocol

from .config import Settings


class ChatJSON(Protocol):
    def chat_json(self, system: str, user: str) -> dict: ...


def _parse_content(content: str) -> dict:
    cleaned = content.strip()
    if cleaned.startswith("```"):
        cleaned = re.sub(r"^```[a-zA-Z]*\s*", "", cleaned)
        cleaned = cleaned.rstrip("`").strip()
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        pass
    # Salvage truncated JSON: scan closing braces from the end and parse the
    # longest valid prefix (LLM output can be cut off at the token limit).
    for idx in range(len(cleaned) - 1, -1, -1):
        if cleaned[idx] == "}":
            try:
                return json.loads(cleaned[: idx + 1])
            except json.JSONDecodeError:
                continue
    # Try closing unclosed arrays/objects with common suffixes.
    for suffix in ("]}", "}", "]}"):
        try:
            return json.loads(cleaned + suffix)
        except json.JSONDecodeError:
            continue
    raise ValueError(f"LLM returned invalid JSON content: {content[:160]!r}")


class LLMClient:
    """OpenAI-compatible chat completions client backed by stdlib urllib.

    Uses raw HTTP instead of the openai SDK: newer SDK transports (httpx2)
    are rejected with 401 by some providers' gateways even when the key,
    URL, headers and body are identical to a working curl request.
    Providers may also transiently return 401 for a valid key on a given
    edge node, so 401 responses are retried with a fresh connection.
    """

    def __init__(self, settings: Settings):
        self._settings = settings

    def chat_json(self, system: str, user: str) -> dict:
        payload = json.dumps({
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            "model": self._settings.model,
            "response_format": {"type": "json_object"},
            "temperature": self._settings.temperature,
            "max_tokens": 8192,
        }).encode("utf-8")
        url = self._settings.base_url.rstrip("/") + "/chat/completions"
        last_detail = ""
        for attempt in range(3):
            req = urllib.request.Request(
                url,
                data=payload,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {self._settings.api_key}",
                    "User-Agent": "cvpaper-eval/0.1",
                },
                method="POST",
            )
            try:
                with urllib.request.urlopen(req, timeout=120) as resp:
                    data = json.loads(resp.read().decode("utf-8"))
                content = data["choices"][0]["message"]["content"]
                return _parse_content(content)
            except urllib.error.HTTPError as e:
                detail = e.read().decode("utf-8", "replace")
                last_detail = f"LLM API error {e.code}: {detail}"
                if e.code == 401 and attempt < 2:
                    time.sleep(1.5 * (attempt + 1))
                    continue
                raise RuntimeError(last_detail) from e
        raise RuntimeError(last_detail)