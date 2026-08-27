from cvpaper_eval.config import Settings
from cvpaper_eval.llm import LLMClient, ChatJSON

def test_chat_json_parses(monkeypatch):
    calls = {}

    class FakeCompletions:
        def create(self, **kwargs):
            calls["kwargs"] = kwargs
            class Msg:
                content = '{"ok": true}'
            class Choice:
                message = Msg()
            class Resp:
                choices = [Choice()]
            return Resp()

    class FakeChat:
        def __init__(self):
            self.chat = type("Chat", (), {"completions": FakeCompletions()})()

    monkeypatch.setattr("cvpaper_eval.llm.OpenAI", lambda **kw: FakeChat())
    settings = Settings(api_key="sk-test")
    client = LLMClient(settings)
    assert client.chat_json("sys", "user") == {"ok": True}
    assert calls["kwargs"]["response_format"] == {"type": "json_object"}
    assert calls["kwargs"]["model"] == "deepseek-chat"
