import json
from pathlib import Path

import pytest

from prompt_builder import load_facts
from response_model import (
    ResponseValidationError,
    build_fact_index,
    build_response_schema,
    parse_structured_reply,
)

ROOT = Path(__file__).resolve().parents[1]
VALID_IDS = set(build_fact_index(load_facts(ROOT / "facts.json")))


def test_schema_restricts_source_ids_to_real_ids():
    schema = build_response_schema(VALID_IDS)
    enum = set(schema["properties"]["source_ids"]["items"]["enum"])
    assert enum == VALID_IDS
    assert schema["additionalProperties"] is False


def test_parses_grounded_reply_and_normalizes_enum_casing():
    raw = json.dumps({
        "answer": "FloorPlan is a decision-support application.",
        "response_type": "Grounded",
        "source_ids": ["proj-fp"],
    })
    reply = parse_structured_reply(raw, VALID_IDS)
    assert reply.response_type == "grounded"
    assert reply.source_ids == ("PROJ-FP",)


def test_rejects_grounded_reply_without_sources():
    raw = json.dumps({"answer": "Claim", "response_type": "grounded", "source_ids": []})
    with pytest.raises(ResponseValidationError):
        parse_structured_reply(raw, VALID_IDS)


def test_allows_unsupported_reply_to_cite_a_verified_pivot():
    raw = json.dumps({"answer": "No. My verified work is in Python.", "response_type": "unsupported", "source_ids": ["SKL-01"]})
    reply = parse_structured_reply(raw, VALID_IDS)
    assert reply.source_ids == ("SKL-01",)


def test_rejects_off_topic_reply_with_sources():
    raw = json.dumps({"answer": "That is outside my verified background.", "response_type": "off_topic", "source_ids": ["PERS-01"]})
    with pytest.raises(ResponseValidationError):
        parse_structured_reply(raw, VALID_IDS)


def test_rejects_unknown_ids_and_extra_fields():
    raw = json.dumps({
        "answer": "Claim",
        "response_type": "grounded",
        "source_ids": ["FAKE-01"],
        "extra": True,
    })
    with pytest.raises(ResponseValidationError):
        parse_structured_reply(raw, VALID_IDS)
