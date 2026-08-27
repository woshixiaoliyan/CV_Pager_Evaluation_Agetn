import os
from cvpaper_eval.config import Settings, load_settings

def test_defaults(monkeypatch):
    monkeypatch.setenv("DEEPSEEK_API_KEY", "sk-test")
    s = load_settings()
    assert s.model == "deepseek-chat"
    assert s.base_url == "https://api.deepseek.com"
    assert s.temperature == 0.1

def test_missing_key_raises(monkeypatch):
    monkeypatch.delenv("DEEPSEEK_API_KEY", raising=False)
    try:
        load_settings()
    except RuntimeError:
        return
    raise AssertionError("expected RuntimeError")
