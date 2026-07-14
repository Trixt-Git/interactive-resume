# WilOS Architecture Specification v2.0

This document supersedes the original Ask Wil v1.x specification. The earlier design used model-written citation tags and broad top-level source labels. Version 2.0 keeps the refusal-first philosophy while replacing that brittle output path with structured responses and exact fact IDs.

## 1. Product goal

Build a short recruiter-facing experience that answers questions about Wil Uhlir accurately and naturally. The system must be useful enough to explain role fit and behavioral examples, but constrained enough that it cannot invent credentials or turn goals into accomplishments.

## 2. Non-negotiable rules

1. `facts.json` is the only factual source.
2. Unsupported professional claims are denied directly.
3. Skills may be claimed only from `skills.confirmed`.
4. Sensitive responses and contact details are not volunteered.
5. Supported personal interests may be answered; preferences not listed in the facts may not be inferred.
6. Every grounded factual answer must cite one or more valid stable fact IDs.
7. Model output is validated before display.
8. No real API key is committed.

## 3. Architecture decisions

| Area | Current choice | Reason |
|---|---|---|
| UI | Streamlit | Fast, deployable, and already part of Wil's working stack |
| Model API | Anthropic Messages API | Strong instruction following with schema-constrained output |
| Default model | `claude-haiku-4-5-20251001` | Appropriate cost and latency for short recruiter conversations |
| Model override | `ANTHROPIC_MODEL` environment variable | Enables controlled A/B testing without code edits |
| Facts | Full JSON injected into system prompt | The corpus is small; retrieval adds failure modes without useful recall gains |
| Output | JSON schema via `output_config.format` | Prevents malformed citation-shaped prose and narrows the response contract |
| Sources | Stable fact IDs | Allows precise validation and readable evidence labels |
| History | Last 12 visible messages | Enough context for short follow-ups without unnecessary token growth |
| Caching | Ephemeral cache control on the system block | Reuses the unchanging fact corpus when provider thresholds are met |
| Tests | pytest plus a separate live evaluation | Separates deterministic code checks from stochastic model behavior |

## 4. Repository structure

```text
wilos/
├── .github/workflows/tests.yml
├── .streamlit/
│   ├── config.toml
│   └── secrets.toml.example
├── tests/
│   ├── test_app_smoke.py
│   ├── test_eval_suite.py
│   ├── test_facts_schema.py
│   ├── test_llm_client.py
│   ├── test_prompt_builder.py
│   └── test_response_model.py
├── pages/1_How_I_Built_This.py
├── app.py
├── BUILD_LOG.md
├── BUILD_MAP.md
├── CLAUDE.md
├── eval_honesty.py
├── facts.json
├── llm_client.py
├── prompt_builder.py
├── README.md
├── requirements.txt
├── requirements-dev.txt
├── response_model.py
├── streamlit_app.py
└── style.py
```

## 5. Facts contract

Every citeable dictionary contains a unique stable `id`. Core records include:

- `ID-01` identity and contact policy
- `NAR-01` career narrative and role fit
- `ROLE-01` current RRD role
- `SKL-01` confirmed and unclaimed skills
- `PROJ-FP` FloorPlan
- `PROJ-WOS` WilOS
- work-history IDs such as `WH-RR`
- personal record `PERS-01`
- sensitive response IDs such as `ST-SAL`
- behavioral story IDs such as `STORY-MYB-DEVELOP`

`response_model.build_fact_index()` recursively discovers IDs and rejects duplicates.

### Skills

`skills.categories` is the organized source of the whitelist, and its flattened values must exactly equal `skills.confirmed`. Every confirmed skill has evidence references to valid IDs.

### FloorPlan

The enterprise version is internal and not public. A separate public portfolio copy demonstrates the approach without exposing company information. The bot must not imply that recruiters can access the enterprise application.

### Disclosure controls

- The contact email is provided only when directly requested; the public facts do not include a phone number.
- Sensitive stored responses are used only for the matching direct question.
- Stories marked `only_when_relevant` are not used as generic color.
- Stories marked `do_not_volunteer` are never surfaced unless the specific question calls for them.

## 6. Prompt contract

The prompt contains five sections:

1. source-of-truth rules
2. boundary rules
3. answer strategy
4. voice guidance
5. structured-response instructions and examples

The answer strategy requires the model to:

- answer in the first sentence
- use the smallest useful evidence set
- choose one behavioral story rather than blending several
- connect evidence to role requirements instead of listing keywords
- stay under 150 words unless asked for detail
- avoid generic “ask me more” closings

## 7. Structured response contract

The model returns exactly:

```json
{
  "answer": "string",
  "response_type": "grounded | unsupported | sensitive | identity | off_topic",
  "source_ids": ["valid-id"]
}
```

Validation rules:

- no extra fields
- non-empty answer
- recognized response type
- no duplicate source IDs
- every source ID must exist in the fact index; broad career answers may cite more than four valid records
- every source ID must exist in the fact index
- `grounded`, `sensitive`, and `identity` require sources
- `off_topic` must have no sources
- provider or validation failures become a safe local `error` reply

## 8. UI and guardrails

- Maximum 60 stored messages, representing 30 exchanges.
- Maximum input length of 1,000 characters.
- The app displays a compact verified-source count with expandable labels derived from exact source IDs.
- Unsupported and off-topic responses receive an “outside verified facts” marker.
- Missing API configuration displays a friendly error rather than throwing an exception.
- The environment variable is checked before Streamlit secrets.

## 9. Evaluation design

### Free deterministic suite

The pytest suite checks:

- facts and evidence integrity
- prompt anchors and current content
- JSON schema construction
- provider-call arguments
- response parsing and source validation
- evaluation coverage
- Streamlit startup with and without configuration

### Live behavioral suite

`eval_honesty.py` contains 29 cases divided into:

- grounding: 8
- answer quality: 5
- conversation: 3
- boundaries: 13

The default is three runs per case, or 87 total model calls. Development runs may use `EVAL_REPEATS=1`. A deploy result is valid only for the exact facts, prompt, model, and code version that produced it.

The July 13, 2026 one-pass production run passed 29/29. The default three-repeat gate has not been run for the current version.

## 10. Definition of done for v2.0

- refined facts are the production `facts.json`
- exact fact IDs replace top-level citation tags
- structured output is validated before display
- supported personal questions work
- unlisted preferences are refused
- story controls guide answer selection
- documentation matches the running architecture
- local tests and Streamlit smoke tests pass
- a new live evaluation is run before publishing a new behavioral score
