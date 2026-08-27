import io
import json
import urllib.error
from cvpaper_eval.config import Settings
from cvpaper_eval.llm import LLMClient

def test_chat_json_parses(monkeypatch):
    captured = {}

    class FakeResp:
        def __init__(self, data):
            self._data = data
        def read(self):
            return self._data
        def __enter__(self):
            return self
        def __exit__(self, *args):
            return False

    def fake_urlopen(req, timeout):
        captured["full_url"] = req.full_url
        captured["method"] = req.get_method()
        captured["auth"] = req.get_header("Authorization")
        captured["body"] = req.data.decode("utf-8")
        return FakeResp(b'{"choices": [{"message": {"content": "{\\"ok\\": true}"}}]}')

    monkeypatch.setattr("cvpaper_eval.llm.urllib.request.urlopen", fake_urlopen)
    settings = Settings(api_key="sk-test")
    client = LLMClient(settings)
    assert client.chat_json("sys", "user") == {"ok": True}
    assert captured["full_url"] == "https://api.deepseek.com/chat/completions"
    assert captured["method"] == "POST"
    assert captured["auth"] == "Bearer sk-test"
    payload = json.loads(captured["body"])
    assert payload["model"] == "deepseek-chat"
    assert payload["response_format"] == {"type": "json_object"}


def test_chat_json_retries_on_401(monkeypatch):
    calls = {"n": 0}

    class FakeResp:
        def read(self):
            return b'{"choices": [{"message": {"content": "{\\"ok\\": true}"}}]}'
        def __enter__(self):
            return self
        def __exit__(self, *args):
            return False

    def fake_urlopen(req, timeout):
        calls["n"] += 1
        if calls["n"] == 1:
            err_body = io.BytesIO(b'{"error": {"message": "invalid"}}')
            raise urllib.error.HTTPError(req.full_url, 401, "Unauthorized", {}, err_body)
        return FakeResp()

    monkeypatch.setattr("cvpaper_eval.llm.urllib.request.urlopen", fake_urlopen)
    client = LLMClient(Settings(api_key="sk-test"))
    assert client.chat_json("sys", "user") == {"ok": True}
    assert calls["n"] == 2

def test_chat_json_salvages_truncated_json(monkeypatch):
    class FakeResp:
        def read(self):
            return b'{"choices": [{"message": {"content": "{\\"metrics\\": [{\\"task\\": \\"a\\"}]} trailing garbage"}}]}'
        def __enter__(self):
            return self
        def __exit__(self, *args):
            return False

    def fake_urlopen(req, timeout):
        return FakeResp()

    monkeypatch.setattr("cvpaper_eval.llm.urllib.request.urlopen", fake_urlopen)
    client = LLMClient(Settings(api_key="sk-test"))
    assert client.chat_json("sys", "user") == {"metrics": [{"task": "a"}]}

def test_chat_json_strips_markdown_fence(monkeypatch):
    class FakeResp:
        def read(self):
            return b'{"choices": [{"message": {"content": "```json\\n{\\"ok\\": true}\\n```"}}]}'
        def __enter__(self):
            return self
        def __exit__(self, *args):
            return False

    def fake_urlopen(req, timeout):
        return FakeResp()

    monkeypatch.setattr("cvpaper_eval.llm.urllib.request.urlopen", fake_urlopen)
    client = LLMClient(Settings(api_key="sk-test"))
    assert client.chat_json("sys", "user") == {"ok": True}

def test_chat_json_salvages_unclosed_array(monkeypatch):
    class FakeResp:
        def read(self):
            return b'{"choices": [{"message": {"content": "{\\"metrics\\": [{\\"task\\": \\"a\\"}, {\\"task\\": \\"b\\"}"}}]}'
        def __enter__(self):
            return self
        def __exit__(self, *args):
            return False

    def fake_urlopen(req, timeout):
        return FakeResp()

    monkeypatch.setattr("cvpaper_eval.llm.urllib.request.urlopen", fake_urlopen)
    client = LLMClient(Settings(api_key="sk-test"))
    assert client.chat_json("sys", "user") == {"metrics": [{"task": "a"}, {"task": "b"}]}