from __future__ import annotations

import json
from typing import Protocol

from openai import OpenAI

from .config import Settings


class ChatJSON(Protocol):
    def chat_json(self, system: str, user: str) -> dict: ...


class LLMClient:
    def __init__(self, settings: Settings):
        self._client = OpenAI(api_key=settings.api_key, base_url=settings.base_url)
        self._model = settings.model
        self._temperature = settings.temperature

    def chat_json(self, system: str, user: str) -> dict:
        response = self._client.chat.completions.create(
            model=self._model,
            temperature=self._temperature,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            response_format={"type": "json_object"},
        )
        content = response.choices[0].message.content
        return json.loads(content)
