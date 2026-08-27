from __future__ import annotations

from ..models import DimensionStatus, EvalReport
from .aggregation import summarize_deltas, summarize_metrics


def _fmt(v) -> str:
    if v is None:
        return "-"
    if isinstance(v, float):
        return f"{v:.2f}"
    return str(v)


def render_markdown(report: EvalReport) -> str:
    lines: list[str] = []
    lines.append(f"# 论文评价报告：{report.paper.title or '(未提供标题)'}")
    lines.append("")
    lines.append(f"- 来源：{report.paper.source.value}；arXiv: {report.paper.arxiv_id or '-'}")
    if report.summary:
        lines.append(f"- 综合评分：{_fmt(report.summary.weighted_score)}/5")
    lines.append("")
    lines.append("## 评价摘要")
    lines.append("")
    if report.summary:
        lines.append(f"- 优势：{('、'.join(report.summary.strengths)) if report.summary.strengths else '无明显优势'}")
        lines.append(f"- 不足：{('、'.join(report.summary.weaknesses)) if report.summary.weaknesses else '无明显不足'}")
        lines.append(f"- 结论：{report.summary.conclusion}")
        lines.append("")

    metric_rows = summarize_metrics(report.metrics)
    lines.append("## 实验指标摘要")
    lines.append("")
    if metric_rows:
        lines.append("| 数据集 | 指标 | 变体 | 本方法最优 | 基线最优 | 差值 | 对比方法数 |")
        lines.append("|---|---|---|---|---|---|---|")
        for r in metric_rows:
            delta = f"{r['delta']:+.2f}" if r["delta"] is not None else "-"
            lines.append(
                f"| {r['dataset']} | {r['metric_name']} | {r['metric_variant'] or '-'} | "
                f"{_fmt(r['ours_best'])} | {_fmt(r['baseline_best'])} | {delta} | "
                f"{r['n_ours'] + r['n_baselines']} |"
            )
    else:
        lines.append("未抽取到可对比的实验指标。")
    if metric_rows and all(r["ours_best"] is None for r in metric_rows):
        lines.append("")
        lines.append("⚠ 未能从论文中识别出“本方法”的实验行（可能为抽取遗漏），差值暂缺。")
    lines.append("")
    lines.append("> 完整指标与对比明细见 report.json。")
    lines.append("")

    lines.append("## 对比结论摘要")
    lines.append("")
    delta_summary = summarize_deltas(metric_rows)
    if delta_summary["compared_groups"]:
        lines.append(
            f"- 有效对比组：{delta_summary['compared_groups']}；平均差值：{delta_summary['mean_delta']:+.2f}；"
            f"范围：{delta_summary['min_delta']:+.2f} ~ {delta_summary['max_delta']:+.2f}"
        )
        if delta_summary["negative"]:
            neg = "、".join(f"{n['metric_name']}({n['dataset']}) {n['delta']:+.2f}" for n in delta_summary["negative"])
            lines.append(f"- 负向指标：{neg} ⚠")
        else:
            lines.append("- 负向指标：无")
    else:
        lines.append("- 无可对比的基线差值。")
    for c in report.comparisons:
        if c.type.value in ("coverage", "statistics", "vs_sota"):
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

    not_evaluated = [d.dimension for d in report.dimension_scores if d.status == DimensionStatus.NOT_EVALUATED]
    review = [d.dimension for d in report.dimension_scores if d.status == DimensionStatus.REVIEW]
    lines.append("## 未评估 / 待审核")
    lines.append("")
    for name in not_evaluated:
        lines.append(f"- {name}：需外部数据，未评估")
    for name in review:
        lines.append(f"- {name}：争议维度，待人工审核")
    return "\n".join(lines)