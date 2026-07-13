"""Structured response contract and fact-id validation for WilOS."""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any, Iterable

MODEL_RESPONSE_TYPES = (
    "grounded",
    "unsupported",
    "sensitive",
    "identity",
    "off_topic",
)


@dataclass(frozen=True)
class LLMReply:
    answer: str
    response_type: str
    source_ids: tuple[str, ...]


class ResponseValidationError(ValueError):
    """Raised when a model response is valid JSON but violates app semantics."""


def iter_fact_entries(node: Any, path: tuple[str, ...] = ()) -> Iterable[tuple[str, dict, tuple[str, ...]]]:
    """Yield every dict containing a stable ``id`` anywhere in the facts tree."""
    if isinstance(node, dict):
        entry_id = node.get("id")
        if isinstance(entry_id, str):
            yield entry_id, node, path
        for key, value in node.items():
            yield from iter_fact_entries(value, path + (key,))
    elif isinstance(node, list):
        for index, value in enumerate(node):
            yield from iter_fact_entries(value, path + (str(index),))


def _entry_label(entry_id: str, entry: dict, path: tuple[str, ...]) -> str:
    if entry.get("name"):
        return str(entry["name"])
    if entry.get("title") and entry.get("employer"):
        return f'{entry["title"]} at {entry["employer"]}'
    if entry.get("credential") and entry.get("institution"):
        return f'{entry["credential"]} at {entry["institution"]}'
    if entry.get("title"):
        return str(entry["title"])
    if entry_id == "ID-01":
        return "Identity and contact information"
    if entry_id == "NAR-01":
        return "Career narrative and role fit"
    if entry_id == "ROLE-01":
        return "Current role at RRD"
    if entry_id == "SKL-01":
        return "Verified skills"
    if entry_id == "PERS-01":
        return "Personal interests"
    if entry_id.startswith("ST-"):
        leaf = path[-1].replace("_", " ") if path else "sensitive topic"
        return leaf.title()
    return entry_id


def build_fact_index(facts: dict) -> dict[str, str]:
    """Return ``fact id -> human label`` and fail fast on duplicate ids."""
    index: dict[str, str] = {}
    for entry_id, entry, path in iter_fact_entries(facts):
        if entry_id in index:
            raise ValueError(f"Duplicate fact id: {entry_id}")
        index[entry_id] = _entry_label(entry_id, entry, path)
    return index


def build_response_schema(valid_source_ids: Iterable[str]) -> dict:
    """Create the JSON schema sent to Claude's structured-output API."""
    ids = sorted(set(valid_source_ids))
    if not ids:
        raise ValueError("At least one valid source id is required")
    return {
        "type": "object",
        "properties": {
            "answer": {"type": "string"},
            "response_type": {"type": "string", "enum": list(MODEL_RESPONSE_TYPES)},
            "source_ids": {
                "type": "array",
                "items": {"type": "string", "enum": ids},
            },
        },
        "required": ["answer", "response_type", "source_ids"],
        "additionalProperties": False,
    }


def parse_structured_reply(raw_text: str, valid_source_ids: Iterable[str]) -> LLMReply:
    """Parse and semantically validate a schema-constrained model response."""
    try:
        payload = json.loads(raw_text)
    except json.JSONDecodeError as exc:
        raise ResponseValidationError("Model response was not valid JSON") from exc

    if not isinstance(payload, dict):
        raise ResponseValidationError("Model response must be a JSON object")
    if set(payload) != {"answer", "response_type", "source_ids"}:
        raise ResponseValidationError("Model response contains unexpected fields")

    answer = payload["answer"]
    response_type = payload["response_type"]
    source_ids = payload["source_ids"]

    if not isinstance(answer, str) or not answer.strip():
        raise ResponseValidationError("Answer must be non-empty text")
    if not isinstance(response_type, str):
        raise ResponseValidationError("response_type must be text")
    response_type = response_type.lower()
    if response_type not in MODEL_RESPONSE_TYPES:
        raise ResponseValidationError(f"Unknown response type: {response_type}")
    if not isinstance(source_ids, list) or not all(isinstance(item, str) for item in source_ids):
        raise ResponseValidationError("source_ids must be a list of strings")
    if len(source_ids) != len(set(source_ids)):
        raise ResponseValidationError("source_ids may not contain duplicates")

    valid = set(valid_source_ids)
    canonical = {item.lower(): item for item in valid}
    source_ids = [canonical.get(item.lower(), item) for item in source_ids]
    if len(source_ids) != len(set(source_ids)):
        raise ResponseValidationError("source_ids may not contain duplicates")
    if len(source_ids) > 4:
        raise ResponseValidationError("source_ids may contain at most four ids")
    unknown = [item for item in source_ids if item not in valid]
    if unknown:
        raise ResponseValidationError(f"Unknown source ids: {', '.join(unknown)}")

    if response_type == "off_topic" and source_ids:
        raise ResponseValidationError("off_topic replies must not cite supporting facts")
    if response_type in {"grounded", "sensitive", "identity"} and not source_ids:
        raise ResponseValidationError(f"{response_type} replies require at least one source id")

    return LLMReply(answer=answer.strip(), response_type=response_type, source_ids=tuple(source_ids))


def error_reply() -> LLMReply:
    return LLMReply(
        answer="Something went wrong on my end. Please try that question again in a moment.",
        response_type="error",
        source_ids=(),
    )
