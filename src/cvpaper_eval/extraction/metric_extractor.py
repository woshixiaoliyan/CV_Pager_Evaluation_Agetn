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
    "Return at most 80 metrics; only include rows with explicit numeric values. Include the proposed method and all its variants first. Also return the top-level field \"proposed_method\": \"<the paper's own method name>\" (e.g. DETR)."
)

RETRY_SUFFIX = (
    " The previous extraction missed rows. Focus on the numeric result tables "
    "(Table 1-5) and extract every reported metric row with explicit values, "
    "including the proposed method and all its variants first."
)


LOWER_DEFAULTS = {
    "fid", "kid", "sfid", "fvd", "epe", "rmse", "absrel", "cer", "ece", "mce",
    "lpips", "niqe", "piqe", "brisque", "musiq",
}
HIGHER_DEFAULTS = {
    "accuracy", "precision", "recall", "f1", "map", "ap", "ap50", "ap75", "aps", "apm", "apl",
    "miou", "iou", "dice", "pq", "sq", "rq", "pqth", "sqth", "rqth", "pqst", "sqst", "rqst",
    "mota", "motp", "idf1", "hota", "psnr", "ssim", "ndcg", "top-1", "top-5", "auc", "pck",
    "pckh", "rank-1", "rank-5", "f1-all", "tar@far", "mrr", "precision@k", "recall@k",
    "balanced-accuracy",
}


def _infer_direction(raw: dict, kb: dict) -> MetricDirection | None:
    """返回指标方向；无法判定时返回 None（调用方应丢弃该行，宁缺毋滥）。"""
    explicit = raw.get("direction")
    if explicit in ("higher", "lower"):
        return MetricDirection(explicit)
    name = raw.get("metric_name", "").lower()
    defaults = kb.get("metric_schema", {}).get("direction_defaults", {})
    if name in defaults:
        return MetricDirection(defaults[name])
    if name in HIGHER_DEFAULTS:
        return MetricDirection.HIGHER
    if name in LOWER_DEFAULTS:
        return MetricDirection.LOWER
    return None


def _normalize_variant(metric_name: str, variant: str) -> str:
    v = (variant or "").strip().lower().replace(" ", "")
    mn = (metric_name or "").strip().lower()
    if mn in ("map", "ap") or "map" in mn:
        if any(s in v for s in ("0.5:0.95", "0.5-0.95", "50:95")):
            return "mAP@0.5:0.95"
        if "0.5" in v:
            return "mAP@0.5"
    return variant.strip()


def _normalize_method_key(method_key: str, proposed: str) -> str:
    mk = method_key.strip().lower()
    if mk in ("ours", "our", "this paper", "proposed"):
        return "Ours"
    if proposed and (mk == proposed.lower() or proposed.lower() in mk or mk in proposed.lower()):
        return "Ours"
    return method_key


def _build_metrics(payload: dict, kb: dict) -> list[Metric]:
    proposed = str(payload.get("proposed_method", "") or "")
    metrics: list[Metric] = []
    for i, raw in enumerate(payload.get("metrics", [])):
        direction = _infer_direction(raw, kb)
        if direction is None:
            continue
        try:
            metrics.append(
                Metric(
                    metric_id=f"M-{i:03d}",
                    task=raw.get("task", ""),
                    dataset=raw.get("dataset", "").strip(),
                    metric_name=raw.get("metric_name", ""),
                    metric_variant=_normalize_variant(raw.get("metric_name", ""), raw.get("metric_variant", "")),
                    value=float(raw["value"]),
                    direction=direction,
                    method_key=_normalize_method_key(raw.get("method_key", ""), proposed),
                    source_location=raw.get("source_location", ""),
                    normalization_note=raw.get("normalization_note") or "",
                )
            )
        except (KeyError, TypeError, ValueError):
            continue
    return metrics


def extract_metrics(chat: ChatJSON, text: str, tables: list[dict], kb: dict) -> list[Metric]:
    user = json.dumps(
        {"text": text[:48000], "tables": tables[:50], "schema": kb.get("metric_schema", {})},
        ensure_ascii=False,
    )
    metrics: list[Metric] = []
    proposed = ""
    for attempt in range(2):
        system = SYSTEM_PROMPT
        if attempt == 1:
            system += RETRY_SUFFIX
            if proposed:
                system += f" The proposed method is '{proposed}'; include its rows."
        payload = chat.chat_json(system, user)
        proposed = str(payload.get("proposed_method", "") or "")
        metrics = _build_metrics(payload, kb)
        has_ours = any(m.method_key == "Ours" for m in metrics)
        if metrics and (has_ours or not proposed):
            break
    return metrics