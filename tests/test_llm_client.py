import json
from types import SimpleNamespace

import llm_client


class FakeMessages:
    def __init__(self, text):
        self.text = text
        self.kwargs = None

    def create(self, **kwargs):
        self.kwargs = kwargs
        return SimpleNamespace(content=[SimpleNamespace(text=self.text)], stop_reason="end_turn")


class FakeClient:
    def __init__(self, text):
        self.messages = FakeMessages(text)


def test_get_reply_uses_structured_output_and_validates_sources(monkeypatch):
    text = json.dumps({
        "answer": "I built FloorPlan.",
        "response_type": "grounded",
        "source_ids": ["PROJ-FP"],
    })
    fake = FakeClient(text)
    client_kwargs = {}

    def fake_anthropic(**kwargs):
        client_kwargs.update(kwargs)
        return fake

    monkeypatch.setattr(llm_client.anthropic, "Anthropic", fake_anthropic)

    reply = llm_client.get_reply("key", "prompt", [{"role": "user", "content": "Question"}], {"PROJ-FP"})

    assert reply.source_ids == ("PROJ-FP",)
    assert fake.messages.kwargs["output_config"]["format"]["type"] == "json_schema"
    assert fake.messages.kwargs["system"][0]["cache_control"] == {"type": "ephemeral"}
    assert client_kwargs["timeout"] == llm_client.REQUEST_TIMEOUT_SECONDS
    assert client_kwargs["max_retries"] == 0


def test_get_reply_returns_safe_error_on_invalid_provider_output(monkeypatch):
    fake = FakeClient("not json")
    monkeypatch.setattr(llm_client.anthropic, "Anthropic", lambda **kwargs: fake)
    monkeypatch.setattr(llm_client.time, "sleep", lambda seconds: None)
    reply = llm_client.get_reply("key", "prompt", [{"role": "user", "content": "Question"}], {"PROJ-FP"})
    assert reply.response_type == "error"
    assert not reply.source_ids


def test_get_reply_retries_invalid_output_once(monkeypatch):
    class RetryMessages:
        def __init__(self):
            self.calls = 0

        def create(self, **kwargs):
            self.calls += 1
            text = "not json" if self.calls == 1 else json.dumps({
                "answer": "I built FloorPlan.",
                "response_type": "grounded",
                "source_ids": ["PROJ-FP"],
            })
            return SimpleNamespace(content=[SimpleNamespace(text=text)])

    fake = SimpleNamespace(messages=RetryMessages())
    monkeypatch.setattr(llm_client.anthropic, "Anthropic", lambda **kwargs: fake)
    monkeypatch.setattr(llm_client.time, "sleep", lambda seconds: None)

    reply = llm_client.get_reply("key", "prompt", [{"role": "user", "content": "Question"}], {"PROJ-FP"})

    assert reply.answer == "I built FloorPlan."
    assert fake.messages.calls == 2
