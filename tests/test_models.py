from cvpaper_eval.models import Metric, MetricDirection, EvalReport, PaperMeta

def test_metric_defaults():
    m = Metric(metric_id="M-001", task="detection", dataset="COCO val2017",
               metric_name="mAP", value=0.482, method_key="Ours", source_location="TABLE 2")
    assert m.direction == MetricDirection.HIGHER

def test_metric_rejects_bad_direction():
    m = Metric(metric_id="M-001", task="detection", dataset="COCO val2017",
               metric_name="FID", value=20.0, direction="lower",
               method_key="Ours", source_location="TABLE 2")
    assert m.direction == MetricDirection.LOWER

def test_report_roundtrip():
    r = EvalReport(paper=PaperMeta(title="T"), sections=[], tables=[], metrics=[],
                   comparisons=[], dimension_scores=[], summary=None)
    assert r.paper.title == "T"
