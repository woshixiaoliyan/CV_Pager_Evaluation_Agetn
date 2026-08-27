from cvpaper_eval.models import Metric
from cvpaper_eval.extraction.validation import validate_metric

def test_out_of_range():
    m = Metric(metric_id="M-1", task="detection", dataset="COCO", metric_name="accuracy", value=1.7, method_key="Ours", source_location="T1")
    assert any("out of range" in e for e in validate_metric(m))

def test_missing_dataset_and_location():
    m = Metric(metric_id="M-2", task="detection", dataset="", metric_name="mAP", value=0.5, method_key="Ours", source_location="")
    errors = validate_metric(m)
    assert len(errors) == 2
