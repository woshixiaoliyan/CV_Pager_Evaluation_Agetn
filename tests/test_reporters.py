import json
from cvpaper_eval.models import EvalReport, PaperMeta, Metric, DimensionScore, Summary, DimensionStatus
from cvpaper_eval.report.markdown_reporter import render_markdown
from cvpaper_eval.report.json_reporter import render_json

def _report():
    return EvalReport(
        paper=PaperMeta(title="T", source="text"),
        metrics=[Metric(metric_id="M-0", metric_name="mAP", value=0.48, method_key="Ours", source_location="T1")],
        dimension_scores=[DimensionScore(cluster_id="CL-001", dimension="创新性", score=4, status=DimensionStatus.EVALUATED),
                          DimensionScore(cluster_id="CL-016", dimension="引文影响力", status=DimensionStatus.NOT_EVALUATED)],
        summary=Summary(weighted_score=4.0, conclusion="ok"),
    )

def test_markdown_contains_sections():
    md = render_markdown(_report())
    assert "# " in md and "mAP" in md and "未评估" in md and "4.0" in md

def test_json_roundtrip():
    data = json.loads(render_json(_report()))
    assert data["paper"]["title"] == "T"


def test_markdown_uses_summary_tables():
    md = render_markdown(_report())
    assert "实验指标摘要" in md
    assert "对比结论摘要" in md
    assert "M-000" not in md

def test_markdown_warns_when_no_ours():
    from cvpaper_eval.models import Metric
    report = _report()
    report.metrics = [Metric(metric_id="M-0", metric_name="mAP", value=0.48, method_key="Faster R-CNN", source_location="T1")]
    md = render_markdown(report)
    assert "未能从论文中识别" in md