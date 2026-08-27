from cvpaper_eval.models import Comparison, DimensionScore, Summary
from cvpaper_eval.scoring.dimension_scorer import score_dimensions, build_summary

class FakeChat:
    def chat_json(self, system, user):
        return {"dimension_scores": [
            {"cluster_id": "CL-001", "score": 4, "confidence": "high", "evidence": ["novel mechanism"]},
            {"cluster_id": "CL-004", "score": 3, "confidence": "medium", "evidence": ["+0.06 vs baseline"]}
        ]}

def test_score_dimensions():
    kb = {"dimensions": [
        {"cluster_id": "CL-001", "name": "创新性/新颖性", "status": "evaluated"},
        {"cluster_id": "CL-004", "name": "技术稳健性", "status": "evaluated"}
    ]}
    scores = score_dimensions(FakeChat(), [], {"novelty_claims": []}, kb)
    assert {s.cluster_id for s in scores} == {"CL-001", "CL-004"}
    assert scores[0].score == 4

def test_build_summary_equal_weights():
    scores = [DimensionScore(cluster_id="CL-001", dimension="A", score=4),
              DimensionScore(cluster_id="CL-004", dimension="B", score=2)]
    summary = build_summary(scores)
    assert summary.weighted_score == 3.0
    assert summary.strengths[0] == "A (4.0)"
    assert summary.weaknesses[0] == "B (2.0)"


def test_score_dimensions_normalizes_numeric_confidence():
    kb = {"dimensions": [
        {"cluster_id": "CL-001", "name": "创新性/新颖性", "status": "evaluated"},
    ]}

    class FakeChatNumeric:
        def chat_json(self, system, user):
            return {"dimension_scores": [
                {"cluster_id": "CL-001", "score": 4, "confidence": 0.9, "evidence": ["x"]}
            ]}

    scores = score_dimensions(FakeChatNumeric(), [], {}, kb)
    assert scores[0].confidence == "high"