import os
from cvpaper_eval.config import Settings, load_settings

def test_defaults(monkeypatch):
    monkeypatch.setenv("DEEPSEEK_API_KEY", "sk-test")
    s = load_settings()
    assert s.model == "deepseek-chat"
    assert s.base_url == "https://api.deepseek.com"
    assert s.temperature == 0.1

def test_missing_key_raises(monkeypatch, tmp_path):
    monkeypatch.delenv("DEEPSEEK_API_KEY", raising=False)
    monkeypatch.chdir(tmp_path)

    try:
        load_settings()
    except RuntimeError:
        return
    raise AssertionError("expected RuntimeError")

def test_loads_key_from_env_file(monkeypatch, tmp_path):
    monkeypatch.delenv("DEEPSEEK_API_KEY", raising=False)
    monkeypatch.chdir(tmp_path)
    (tmp_path / ".env").write_text("DEEPSEEK_API_KEY=sk-from-env-file\n", encoding="utf-8")
    monkeypatch.chdir(tmp_path)
    s = load_settings()
    assert s.api_key == "sk-from-env-file"