from pathlib import Path
from cvpaper_eval.knowledge_base import load_knowledge_base

def test_seed_kb_loads():
    kb = load_knowledge_base(Path("knowledge_base/indicators_v1.json"))
    dims = kb["dimensions"]
    assert len(dims) == 14
    assert {d["cluster_id"] for d in dims} >= {"CL-001", "CL-009", "CL-015"}
    for d in dims:
        assert d["name"] and d["question"] and d["criteria_high"] and d["criteria_low"]
    assert len(kb["mapping"]) >= 10
    assert kb["metric_schema"]["variant_notes"]["mAP@0.5:0.95"]
