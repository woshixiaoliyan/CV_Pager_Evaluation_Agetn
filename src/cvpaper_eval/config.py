from __future__ import annotations

import os
import tempfile
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Settings:
    api_key: str
    base_url: str = "https://api.deepseek.com"
    model: str = "deepseek-chat"
    temperature: float = 0.1
    kb_path: Path = Path("knowledge_base/indicators_v1.json")
    tmp_dir: Path = Path(tempfile.gettempdir()) / "cvpaper_eval"


def _load_env_key() -> str:
    env_path = Path(".env")
    if not env_path.exists():
        return ""
    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line.startswith("DEEPSEEK_API_KEY="):
            return line.split("=", 1)[1].strip().strip('"').strip("'")
    return ""


def load_settings() -> Settings:
    api_key = os.environ.get("DEEPSEEK_API_KEY", "") or _load_env_key()
    if not api_key:
        raise RuntimeError("DEEPSEEK_API_KEY is not set (env or .env)")
    return Settings(api_key=api_key)