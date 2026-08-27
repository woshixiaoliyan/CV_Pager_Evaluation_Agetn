from cvpaper_eval.extraction.qualitative_extractor import extract_qualitative, KEYS

class FakeChat:
    def chat_json(self, system, user):
        return {"novelty_claims": [{"text": "We propose a new paradigm.", "location": "SEC-001"}],
                "limitations": [], "openness": [], "ethics": [], "related_work": [], "clarity": []}

def test_extract_qualitative_keys():
    out = extract_qualitative(FakeChat(), "text", {})
    assert set(out) == set(KEYS)
    assert out["novelty_claims"][0]["location"] == "SEC-001"
