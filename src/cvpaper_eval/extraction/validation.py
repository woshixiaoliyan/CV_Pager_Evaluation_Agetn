from __future__ import annotations

from ..models import Metric

RANGES: dict[str, tuple[float, float]] = {
    "accuracy": (0.0, 1.0),
    "precision": (0.0, 1.0),
    "recall": (0.0, 1.0),
    "f1": (0.0, 1.0),
    "map": (0.0, 1.0),
    "miou": (0.0, 1.0),
    "iou": (0.0, 1.0),
    "ssim": (0.0, 1.0),
    "psnr": (0.0, 100.0),
    "fid": (0.0, 1000.0),
    "fps": (0.0, 100000.0),
}


def validate_metric(metric: Metric) -> list[str]:
    errors: list[str] = []
    key = metric.metric_name.lower()
    if key in RANGES:
        lo, hi = RANGES[key]
        if not (lo <= metric.value <= hi):
            errors.append(f"{metric.metric_name} value {metric.value} out of range [{lo}, {hi}]")
    if not metric.dataset:
        errors.append("dataset is required for comparison")
    if not metric.source_location:
        errors.append("source_location is required for traceability")
    return errors
