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

class FakeChatProposed:
    def chat_json(self, system, user):
        return {
            "proposed_method": "DETR",
            "metrics": [
                {"task": "detection", "dataset": "COCO", "metric_name": "AP", "value": 44.9, "method_key": "DETR-DC5", "source_location": "T1", "normalization_note": None},
                {"task": "detection", "dataset": "COCO", "metric_name": "AP", "value": 42.0, "method_key": "DETR", "source_location": "T1", "normalization_note": None},
                {"task": "detection", "dataset": "COCO", "metric_name": "AP", "value": 39.0, "method_key": "Faster R-CNN", "source_location": "T1", "normalization_note": None}
            ]
        }

def test_extract_metrics_normalizes_proposed_method():
    kb = {"metric_schema": {"direction_defaults": {}}}
    metrics = extract_metrics(FakeChatProposed(), "text", [], kb)
    ours = [m for m in metrics if m.method_key == "Ours"]
    assert len(ours) == 2
    assert metrics[2].method_key == "Faster R-CNN"

class FakeChatNoOursFirst:
    def __init__(self):
        self.calls = 0
    def chat_json(self, system, user):
        self.calls += 1
        base = {"task": "detection", "dataset": "COCO", "metric_name": "AP", "value": 39.0, "method_key": "Faster RCNN-DC5", "source_location": "T1", "normalization_note": None}
        if self.calls == 1:
            return {"proposed_method": "DETR", "metrics": [base]}
        detr = {"task": "detection", "dataset": "COCO", "metric_name": "AP", "value": 44.9, "method_key": "DETR-DC5", "source_location": "T1", "normalization_note": None}
        return {"proposed_method": "DETR", "metrics": [base, detr]}

def test_extract_metrics_retries_when_no_ours():
    kb = {"metric_schema": {"direction_defaults": {}}}
    fake = FakeChatNoOursFirst()
    metrics = extract_metrics(fake, "text", [], kb)
    assert fake.calls == 2
    assert any(m.method_key == "Ours" for m in metrics)

def test_extract_metrics_normalizes_variant_and_drops_unresolved_direction():
    class FakeChatMixed:
        def chat_json(self, system, user):
            return {
                "proposed_method": "Ours",
                "metrics": [
                    {"task": "detection", "dataset": " COCO ", "metric_name": "mAP", "metric_variant": "mAP@0.5:0.95", "value": 0.482, "method_key": "Ours", "source_location": "T1"},
                    {"task": "detection", "dataset": "COCO", "metric_name": "mAP", "metric_variant": "0.5:0.95", "value": 0.421, "method_key": "Base", "source_location": "T1"},
                    {"task": "detection", "dataset": "COCO", "metric_name": "zzzmetric", "value": 1.0, "method_key": "Ours", "source_location": "T1"}
                ]
            }

    kb = {"metric_schema": {"direction_defaults": {}}}
    metrics = extract_metrics(FakeChatMixed(), "text", [], kb)
    assert len(metrics) == 2
    assert metrics[0].metric_variant == metrics[1].metric_variant
    assert metrics[0].dataset == "COCO"