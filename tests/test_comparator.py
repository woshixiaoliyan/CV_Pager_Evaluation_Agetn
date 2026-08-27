from cvpaper_eval.models import Metric, ComparisonType
from cvpaper_eval.comparison.comparator import build_comparisons

def _m(mid, name, value, method, variant="", dataset="COCO val2017"):
    return Metric(metric_id=mid, task="detection", dataset=dataset, metric_name=name,
                  metric_variant=variant, value=value, method_key=method, source_location="TABLE 2")

def test_vs_baseline_delta():
    ms = [_m("M-0", "mAP", 0.482, "Ours"), _m("M-1", "mAP", 0.421, "Faster R-CNN")]
    cmps = build_comparisons(ms)
    vs = [c for c in cmps if c.type == ComparisonType.VS_BASELINE]
    assert len(vs) == 1
    assert "+0.06" in vs[0].conclusion

def test_coverage_and_consistency():
    ms = [_m("M-0", "mAP", 0.5, "Ours", dataset="COCO"), _m("M-1", "mAP", 0.6, "Ours", dataset="VOC")]
    cmps = build_comparisons(ms)
    assert any(c.type == ComparisonType.COVERAGE and "2 datasets" in c.conclusion for c in cmps)
    assert any(c.type == ComparisonType.CONSISTENCY for c in cmps)
