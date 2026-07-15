"""The single Claude API seam for WilOS."""

from __future__ import annotations

import os
import time

import anthropic

from response_model import (
    LLMReply,
    ResponseValidationError,
    build_response_schema,
    error_reply,
    parse_structured_reply,
)

DEFAULT_MODEL = "claude-haiku-4-5-20251001"
MODEL = os.getenv("ANTHROPIC_MODEL", DEFAULT_MODEL)
REQUEST_TIMEOUT_SECONDS = 15.0
MAX_ATTEMPTS = 2

RETRYABLE_ERRORS = (
    anthropic.APIConnectionError,
    anthropic.APITimeoutError,
    anthropic.RateLimitError,
    anthropic.InternalServerError,
    ResponseValidationError,
)


def get_reply(
    api_key: str,
    system_prompt: str,
    messages: list[dict],
    valid_source_ids: set[str] | list[str] | tuple[str, ...],
) -> LLMReply:
    """Return a validated, structured reply or a safe application error."""
    client = anthropic.Anthropic(
        api_key=api_key,
        timeout=REQUEST_TIMEOUT_SECONDS,
        max_retries=0,
    )
    for attempt in range(1, MAX_ATTEMPTS + 1):
        try:
            response = client.messages.create(
                model=MODEL,
                max_tokens=600,
                temperature=0.5,
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
            retryable = isinstance(exc, RETRYABLE_ERRORS)
            print(
                f"[llm_client] attempt={attempt}/{MAX_ATTEMPTS} "
                f"retryable={retryable} {type(exc).__name__}: {exc}",
                flush=True,
            )
            if not retryable or attempt == MAX_ATTEMPTS:
                return error_reply()
            time.sleep(0.5)

    return error_reply()
