from __future__ import annotations

from ..models import DimensionStatus, EvalReport


def render_markdown(report: EvalReport) -> str:
    lines: list[str] = []
    lines.append(f"# 论文评价报告：{report.paper.title or '(未提供标题)'}")
    lines.append("")
    lines.append(f"- 来源：{report.paper.source.value}；arXiv: {report.paper.arxiv_id or '-'}")
    lines.append(f"- 综合评分：{report.summary.weighted_score if report.summary else '-'}/5")
    lines.append("")
    lines.append("## 实验指标")
    lines.append("")
    lines.append("| ID | 指标 | 数值 | 方法 | 数据集 | 来源 |")
    lines.append("|---|---|---|---|---|---|")
    for m in report.metrics:
        lines.append(f"| {m.metric_id} | {m.metric_name} | {m.value} | {m.method_key} | {m.dataset} | {m.source_location} |")
    lines.append("")
    lines.append("## 对比结论")
    lines.append("")
    for c in report.comparisons:
        lines.append(f"- [{c.type.value}] {c.conclusion}")
    lines.append("")
    lines.append("## 维度得分")
    lines.append("")
    lines.append("| 维度 | 得分 | 置信度 | 证据 |")
    lines.append("|---|---|---|---|")
    for d in report.dimension_scores:
        score = f"{d.score}" if d.score is not None else "-"
        lines.append(f"| {d.dimension} | {score} | {d.confidence} | {'；'.join(d.evidence) or '-'} |")
    lines.append("")
    if report.summary:
        lines.append("## 优势")
        for s in report.summary.strengths:
            lines.append(f"- {s}")
        lines.append("")
        lines.append("## 不足")
        for w in report.summary.weaknesses:
            lines.append(f"- {w}")
        lines.append("")
        lines.append("## 综合结论")
        lines.append("")
        lines.append(report.summary.conclusion)
        lines.append("")
    not_evaluated = [d.dimension for d in report.dimension_scores if d.status == DimensionStatus.NOT_EVALUATED]
    review = [d.dimension for d in report.dimension_scores if d.status == DimensionStatus.REVIEW]
    lines.append("## 未评估 / 待审核")
    lines.append("")
    for name in not_evaluated:
        lines.append(f"- {name}：需外部数据，未评估")
    for name in review:
        lines.append(f"- {name}：争议维度，待人工审核")
    return "\n".join(lines)
