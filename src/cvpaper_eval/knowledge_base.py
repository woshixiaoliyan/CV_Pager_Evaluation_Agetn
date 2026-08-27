from __future__ import annotations

import json
from pathlib import Path


def load_knowledge_base(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)
