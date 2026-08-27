from __future__ import annotations

import json

from ..llm import ChatJSON
from ..models import Metric, MetricDirection

SYSTEM_PROMPT = (
    "You extract quantitative evaluation metrics from computer vision papers. "
    'Return a compact JSON object (no pretty-printing or newlines) with key "metrics": '
    "a list of objects with fields: "
    "task, dataset, metric_name, metric_variant, value (float), direction "
    '("higher" or "lower"), method_key, source_location, normalization_note. '
    "Include every metric found, including baselines and SOTA claims. "
    "Return at most 60 metrics; only include rows with explicit numeric values. Label the paper's own proposed method as method_key='Ours' (never for baselines)."
)

RETRY_SUFFIX = (
    " The previous extraction returned no metrics. Focus on the numeric result "
    "tables (Table 1-5) and extract every reported metric row with explicit values."
)


def _infer_direction(raw: dict, kb: dict) -> MetricDirection:
    explicit = raw.get("direction")
    if explicit in ("higher", "lower"):
        return MetricDirection(explicit)
    defaults = kb.get("metric_schema", {}).get("direction_defaults", {})
    return MetricDirection(defaults.get(raw.get("metric_name", "").lower(), "higher"))


def _build_metrics(payload: dict, kb: dict) -> list[Metric]:
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
                    normalization_note=raw.get("normalization_note") or "",
                )
            )
        except (KeyError, TypeError, ValueError):
            continue
    return metrics


def extract_metrics(chat: ChatJSON, text: str, tables: list[dict], kb: dict) -> list[Metric]:
    user = json.dumps(
        {"text": text[:24000], "tables": tables[:50], "schema": kb.get("metric_schema", {})},
        ensure_ascii=False,
    )
    metrics: list[Metric] = []
    for attempt in range(2):
        system = SYSTEM_PROMPT + (RETRY_SUFFIX if attempt == 1 else "")
        payload = chat.chat_json(system, user)
        metrics = _build_metrics(payload, kb)
        if metrics:
            break
    return metrics