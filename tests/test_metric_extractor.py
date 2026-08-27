from cvpaper_eval.extraction.metric_extractor import extract_metrics

class FakeChat:
    def chat_json(self, system, user):
        return {"metrics": [
            {"task": "detection", "dataset": "COCO val2017", "metric_name": "mAP", "metric_variant": "0.5:0.95", "value": 0.482, "method_key": "Ours", "source_location": "TABLE 2", "normalization_note": ""},
            {"task": "detection", "dataset": "COCO val2017", "metric_name": "mAP", "metric_variant": "0.5:0.95", "value": 0.421, "method_key": "Faster R-CNN", "source_location": "TABLE 2", "normalization_note": ""}
        ]}

def test_extract_metrics():
    kb = {"metric_schema": {"direction_defaults": {}}}
    metrics = extract_metrics(FakeChat(), "text", [], kb)
    assert len(metrics) == 2
    assert metrics[0].metric_id == "M-000"
    assert metrics[0].value == 0.482
    assert metrics[1].method_key == "Faster R-CNN"


class FakeChatEmptyFirst:
    def __init__(self):
        self.calls = 0
    def chat_json(self, system, user):
        self.calls += 1
        if self.calls == 1:
            return {"metrics": []}
        return {"metrics": [
            {"task": "detection", "dataset": "COCO val2017", "metric_name": "mAP", "metric_variant": "0.5:0.95", "value": 0.482, "method_key": "Ours", "source_location": "TABLE 2", "normalization_note": None}
        ]}

def test_extract_metrics_retries_on_empty():
    kb = {"metric_schema": {"direction_defaults": {}}}
    metrics = extract_metrics(FakeChatEmptyFirst(), "text", [], kb)
    assert len(metrics) == 1
    assert metrics[0].value == 0.482
    assert metrics[0].normalization_note == ""