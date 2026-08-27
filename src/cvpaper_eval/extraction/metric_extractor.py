from __future__ import annotations

import json

from ..llm import ChatJSON
from ..models import Metric, MetricDirection

SYSTEM_PROMPT = (
    "You extract quantitative evaluation metrics from computer vision papers. "
    'Return a JSON object with key "metrics": a list of objects with fields: '
    "task, dataset, metric_name, metric_variant, value (float), direction "
    '("higher" or "lower"), method_key, source_location, normalization_note. '
    "Include every metric found, including baselines and SOTA claims."
)


def _infer_direction(raw: dict, kb: dict) -> MetricDirection:
    explicit = raw.get("direction")
    if explicit in ("higher", "lower"):
        return MetricDirection(explicit)
    defaults = kb.get("metric_schema", {}).get("direction_defaults", {})
    return MetricDirection(defaults.get(raw.get("metric_name", "").lower(), "higher"))


def extract_metrics(chat: ChatJSON, text: str, tables: list[dict], kb: dict) -> list[Metric]:
    user = json.dumps(
        {"text": text[:12000], "tables": tables[:50], "schema": kb.get("metric_schema", {})},
        ensure_ascii=False,
    )
    payload = chat.chat_json(SYSTEM_PROMPT, user)
    metrics: list[Metric] = []
    for i, raw in enumerate(payload.get("metrics", [])):
        try:
            metrics.append(
                Metric(
                    metric_id=f"M-{i:03d}",
                    task=raw.get("task", ""),
                    dataset=raw.get("dataset", ""),
                    metric_name=raw.get("metric_name", ""),
                    metric_variant=raw.get("metric_variant", ""),
                    value=float(raw["value"]),
                    direction=_infer_direction(raw, kb),
                    method_key=raw.get("method_key", ""),
                    source_location=raw.get("source_location", ""),
                    normalization_note=raw.get("normalization_note", ""),
                )
            )
        except (KeyError, TypeError, ValueError):
            continue
    return metrics
