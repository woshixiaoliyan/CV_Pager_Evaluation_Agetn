from cvpaper_eval.models import Metric, MetricDirection
from cvpaper_eval.report.aggregation import summarize_metrics, summarize_deltas

def _m(mid, name, value, method, dataset="COCO", direction=MetricDirection.HIGHER, variant=""):
    return Metric(metric_id=mid, task="detection", dataset=dataset, metric_name=name,
                  metric_variant=variant, value=value, direction=direction,
                  method_key=method, source_location="T1")

def test_summarize_metrics_higher_is_better():
    ms = [_m("M-0", "AP", 44.9, "Ours"), _m("M-1", "AP", 42.0, "DETR-DC5"),
          _m("M-2", "AP", 39.0, "Faster R-CNN")]
    rows = summarize_metrics(ms)
    assert len(rows) == 1
    r = rows[0]
    assert r["ours_best"] == 44.9
    assert r["baseline_best"] == 42.0
    assert r["delta"] == 2.9
    assert r["n_baselines"] == 2

def test_summarize_metrics_lower_is_better():
    ms = [_m("M-0", "FID", 20.0, "Ours", direction=MetricDirection.LOWER),
          _m("M-1", "FID", 25.0, "Base", direction=MetricDirection.LOWER)]
    r = summarize_metrics(ms)[0]
    assert r["ours_best"] == 20.0
    assert r["baseline_best"] == 25.0
    assert r["delta"] == 5.0

def test_summarize_deltas_negative():
    rows = [
        {"dataset": "COCO", "metric_name": "AP", "delta": 2.9},
        {"dataset": "COCO", "metric_name": "APS", "delta": -1.0},
    ]
    out = summarize_deltas(rows)
    assert out["mean_delta"] == 0.95
    assert len(out["negative"]) == 1
    assert out["negative"][0]["metric_name"] == "APS"