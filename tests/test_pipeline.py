from pathlib import Path
from cvpaper_eval.config import Settings
from cvpaper_eval.pipeline import run_evaluation

class FakeChat:
    def __init__(self):
        self.calls = 0
    def chat_json(self, system, user):
        self.calls += 1
        if self.calls == 1:
            return {"metrics": [
                {"task": "detection", "dataset": "COCO val2017", "metric_name": "mAP", "metric_variant": "0.5:0.95", "value": 0.482, "method_key": "Ours", "source_location": "TABLE 2", "normalization_note": ""},
                {"task": "detection", "dataset": "COCO val2017", "metric_name": "mAP", "metric_variant": "0.5:0.95", "value": 0.421, "method_key": "Faster R-CNN", "source_location": "TABLE 2", "normalization_note": ""}
            ]}
        if self.calls == 2:
            return {"novelty_claims": [{"text": "new paradigm", "location": "SEC-001"}], "limitations": [], "openness": [], "ethics": [], "related_work": [], "clarity": []}
        return {"dimension_scores": [{"cluster_id": "CL-001", "score": 4, "confidence": "high", "evidence": ["new paradigm"]}]}

def test_run_evaluation_text(monkeypatch, tmp_path):
    from cvpaper_eval import pipeline
    monkeypatch.setattr(pipeline, "LLMClient", lambda settings: FakeChat())
    settings = Settings(api_key="sk-test", kb_path=Path("knowledge_base/indicators_v1.json"))
    text = "Abstract\nWe propose OursNet.\nExperiments\nmAP 0.482 vs 0.421.\nConclusion\nGood."
    report = run_evaluation(text, "text", settings)
    assert len(report.metrics) == 2
    assert report.comparisons
    assert report.summary.weighted_score is not None
    assert any(d.status.value == "not_evaluated" for d in report.dimension_scores)
