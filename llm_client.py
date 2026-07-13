"""The single Claude API seam for WilOS."""

from __future__ import annotations

import os

import anthropic

from response_model import LLMReply, build_response_schema, error_reply, parse_structured_reply

DEFAULT_MODEL = "claude-haiku-4-5-20251001"
MODEL = os.getenv("ANTHROPIC_MODEL", DEFAULT_MODEL)


def get_reply(
    api_key: str,
    system_prompt: str,
    messages: list[dict],
    valid_source_ids: set[str] | list[str] | tuple[str, ...],
) -> LLMReply:
    """Return a validated, structured reply or a safe application error."""
    try:
        client = anthropic.Anthropic(api_key=api_key)
        response = client.messages.create(
            model=MODEL,
            max_tokens=600,
            temperature=0.2,
            system=[
                {
                    "type": "text",
                    "text": system_prompt,
                    "cache_control": {"type": "ephemeral"},
                }
            ],
            messages=messages,
            output_config={
                "format": {
                    "type": "json_schema",
                    "schema": build_response_schema(valid_source_ids),
                }
            },
        )
        return parse_structured_reply(response.content[0].text, valid_source_ids)
    except Exception as exc:  # The UI must not leak provider or validation details.
        print(f"[llm_client] {type(exc).__name__}: {exc}")
        return error_reply()
