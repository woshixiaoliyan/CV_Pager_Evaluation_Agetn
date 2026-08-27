from __future__ import annotations

from collections import defaultdict

from ..models import Comparison, ComparisonType, Metric, MetricDirection

OURS_KEYS = {"ours", "our", "this paper", "proposed", "ours"}


def _group_key(m: Metric) -> tuple[str, str, str, str]:
    return (m.task, m.dataset, m.metric_name, m.metric_variant)


def is_ours(m: Metric) -> bool:
    return m.method_key.strip().lower() in OURS_KEYS


def build_comparisons(metrics: list[Metric]) -> list[Comparison]:
    comparisons: list[Comparison] = []
    groups: dict[tuple, list[Metric]] = defaultdict(list)
    for m in metrics:
        groups[_group_key(m)].append(m)

    for key in sorted(groups):
        group = groups[key]
        ours = [m for m in group if is_ours(m)]
        others = [m for m in group if not is_ours(m)]
        for m in ours:
            for other in others:
                delta = m.value - other.value if m.direction == MetricDirection.HIGHER else other.value - m.value
                comparisons.append(
                    Comparison(
                        comparison_id=f"CMP-{len(comparisons) + 1:03d}",
                        metric_ids=[m.metric_id, other.metric_id],
                        type=ComparisonType.VS_BASELINE,
                        conclusion=f"{m.metric_name} {delta:+.2f} vs {other.method_key} ({m.dataset})",
                        evidence_locations=[m.source_location, other.source_location],
                    )
                )

    datasets = sorted({m.dataset for m in metrics if m.dataset})
    if datasets:
        comparisons.append(
            Comparison(
                comparison_id=f"CMP-{len(comparisons) + 1:03d}",
                type=ComparisonType.COVERAGE,
                conclusion=f"covers {len(datasets)} datasets: {', '.join(datasets)}",
            )
        )

    if len(datasets) >= 2:
        comparisons.append(
            Comparison(
                comparison_id=f"CMP-{len(comparisons) + 1:03d}",
                type=ComparisonType.CONSISTENCY,
                conclusion=f"reported across {len(datasets)} datasets",
            )
        )

    disclosed = any("std" in (m.normalization_note + " " + m.metric_variant).lower() for m in metrics)
    comparisons.append(
        Comparison(
            comparison_id=f"CMP-{len(comparisons) + 1:03d}",
            type=ComparisonType.STATISTICS,
            conclusion="reports variance/std disclosure" if disclosed else "no variance/std disclosure detected",
            metric_ids=[m.metric_id for m in metrics],
        )
    )
    return comparisons
