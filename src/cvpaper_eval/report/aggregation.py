from __future__ import annotations

from collections import defaultdict

from ..comparison.comparator import is_ours
from ..models import Metric, MetricDirection


def _best(metrics: list[Metric], direction: MetricDirection) -> tuple[float | None, str | None]:
    if not metrics:
        return None, None
    if direction == MetricDirection.HIGHER:
        best = max(metrics, key=lambda m: m.value)
    else:
        best = min(metrics, key=lambda m: m.value)
    return best.value, best.method_key


def summarize_metrics(metrics: list[Metric]) -> list[dict]:
    """按 (数据集, 指标名, 变体) 分组，输出本方法最优 vs 基线最优的汇总行。"""
    groups: dict[tuple, list[Metric]] = defaultdict(list)
    for m in metrics:
        groups[(m.dataset, m.metric_name, m.metric_variant)].append(m)

    rows: list[dict] = []
    for (dataset, name, variant), group in sorted(groups.items()):
        direction = group[0].direction
        ours = [m for m in group if is_ours(m)]
        baselines = [m for m in group if not is_ours(m)]
        ours_best, ours_method = _best(ours, direction)
        base_best, base_method = _best(baselines, direction)
        delta = None
        if ours_best is not None and base_best is not None:
            if direction == MetricDirection.HIGHER:
                delta = round(ours_best - base_best, 2)
            else:
                delta = round(base_best - ours_best, 2)
        rows.append({
            "dataset": dataset,
            "metric_name": name,
            "metric_variant": variant,
            "direction": direction.value,
            "ours_best": ours_best,
            "ours_best_method": ours_method,
            "baseline_best": base_best,
            "baseline_best_method": base_method,
            "delta": delta,
            "n_ours": len(ours),
            "n_baselines": len(baselines),
        })
    return rows


def summarize_deltas(rows: list[dict]) -> dict:
    deltas = [r["delta"] for r in rows if r["delta"] is not None]
    negative = [r for r in rows if r["delta"] is not None and r["delta"] < 0]
    return {
        "compared_groups": len(deltas),
        "mean_delta": round(sum(deltas) / len(deltas), 2) if deltas else None,
        "min_delta": min(deltas) if deltas else None,
        "max_delta": max(deltas) if deltas else None,
        "negative": [
            {"dataset": r["dataset"], "metric_name": r["metric_name"], "delta": r["delta"]}
            for r in negative
        ],
    }