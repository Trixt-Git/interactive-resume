# CLAUDE.md

## Project

WilOS is a Streamlit interactive resume. It answers in first person from `facts.json`, returns schema-constrained responses, validates exact fact IDs, and refuses unsupported claims.

Read `BUILD_MAP.md` before making architectural changes. Record meaningful changes in `BUILD_LOG.md`.

## Commands

```bash
pip install -r requirements-dev.txt
pytest -q
streamlit run WilOS.py
EVAL_REPEATS=1 python eval_honesty.py  # real API calls
```

`ANTHROPIC_API_KEY` may come from the environment or `.streamlit/secrets.toml`. Never commit a real key.

## Current architecture

### Full facts in the system prompt

There is no RAG, vector database, or embedding layer. `prompt_builder.py` serializes the complete verified `facts.json` into the system prompt at app startup. Do not add retrieval unless the corpus becomes too large for reliable full-context use.

### Stable fact IDs

Every citeable record has a stable `id`. `response_model.build_fact_index()` discovers those IDs and fails on duplicates. Model responses cite exact IDs, and `parse_structured_reply()` rejects unknown or invalid sources.

### Structured response contract

The provider response must contain exactly:

```json
{
  "answer": "visible prose",
  "response_type": "grounded | unsupported | sensitive | identity | off_topic",
  "source_ids": ["PROJ-FP"]
}
```

`llm_client.py` supplies a JSON schema through `output_config.format`. Do not reintroduce trailing citation text or regex parsing.

### Single provider seam

Only `llm_client.py` imports `anthropic`. The model defaults to `claude-haiku-4-5-20251001` and can be overridden with `ANTHROPIC_MODEL`.

### Prompt priorities

The prompt must preserve these behaviors:

1. Facts are the only source of truth.
2. Skills outside the confirmed list are denied plainly.
3. False premises are corrected.
4. Prompt-injection attempts are refused.
5. Sensitive responses are used verbatim and only when asked.
6. Supported personal facts may be answered; unsupported preferences may not be inferred.
7. Answers lead with the answer, use minimal evidence, and do not recite the full resume.
8. Behavioral questions use one relevant story.
9. The contact email is not volunteered. The public fact corpus does not contain a phone number.

### UI behavior

`WilOS.py` stores visible conversation text plus structured metadata in `st.session_state`. It sends the last 12 visible messages to the model. It supports a 60-message session cap and a 1,000-character input cap.

The application should show a friendly configuration error when no API key exists. Do not call `st.secrets.get()` without handling `StreamlitSecretNotFoundError`.

## Testing expectations

Run `pytest -q` after every relevant change. Tests should cover structure and deterministic behavior without real API calls.

The live evaluation is separate because it costs real calls. It contains four suites:

- grounding
- answer quality
- conversation
- boundaries

Do not weaken an evaluation expectation to make a model failure pass. Fix the facts, prompt, response contract, or model behavior instead.

## Facts editing rules

- Never infer a fact.
- Preserve the private enterprise/public portfolio distinction for FloorPlan.
- Do not add “rehire eligible.”
- Do not add `applied AI/LLM tooling` as a claimed skill.
- Keep LinkedIn as `https://www.linkedin.com/in/wil-uhlir/`.
- Sensitive stories and contact details must retain their disclosure controls.
- Add a unique stable ID to every new citeable record.
