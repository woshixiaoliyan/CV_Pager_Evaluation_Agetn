from __future__ import annotations

from ..models import EvalReport


def render_json(report: EvalReport) -> str:
    return report.model_dump_json(indent=2)
