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
    monkeypatch.setattr(llm_client.anthropic, "Anthropic", lambda api_key: fake)

    reply = llm_client.get_reply("key", "prompt", [{"role": "user", "content": "Question"}], {"PROJ-FP"})

    assert reply.source_ids == ("PROJ-FP",)
    assert fake.messages.kwargs["output_config"]["format"]["type"] == "json_schema"
    assert fake.messages.kwargs["system"][0]["cache_control"] == {"type": "ephemeral"}


def test_get_reply_returns_safe_error_on_invalid_provider_output(monkeypatch):
    fake = FakeClient("not json")
    monkeypatch.setattr(llm_client.anthropic, "Anthropic", lambda api_key: fake)
    reply = llm_client.get_reply("key", "prompt", [{"role": "user", "content": "Question"}], {"PROJ-FP"})
    assert reply.response_type == "error"
    assert not reply.source_ids
