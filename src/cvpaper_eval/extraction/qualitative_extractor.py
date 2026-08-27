from __future__ import annotations

import json

from ..llm import ChatJSON

KEYS = ["novelty_claims", "limitations", "openness", "ethics", "related_work", "clarity"]

SYSTEM_PROMPT = (
    "Extract qualitative evaluation evidence from a computer vision paper. "
    'Return a JSON object with keys: novelty_claims, limitations, openness, ethics, related_work, clarity. '
    'Each value is a list of {"text": str, "location": str}. '
    "Only include sentences actually present in the paper text."
)


def extract_qualitative(chat: ChatJSON, text: str, kb: dict) -> dict:
    user = json.dumps({"text": text[:16000], "dimensions": kb.get("dimensions", [])}, ensure_ascii=False)
    payload = chat.chat_json(SYSTEM_PROMPT, user)
    out = {}
    for key in KEYS:
        items = payload.get(key, [])
        out[key] = [{"text": str(i.get("text", "")), "location": str(i.get("location", ""))} for i in items if isinstance(i, dict)]
    return out
