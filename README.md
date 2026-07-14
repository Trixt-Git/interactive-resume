# WilOS

WilOS is a recruiter-facing interactive resume built with Streamlit and the Anthropic API. It answers questions about Wil Uhlir from one verified `facts.json` file, cites the exact fact records used, and refuses unsupported claims rather than filling gaps.

**Live app:** [wilresume.streamlit.app](https://wilresume.streamlit.app/)

## Current design

- **Full fact injection, not RAG.** The corpus is one person's background and fits comfortably in the model context, so the complete verified record is compiled into the system prompt at startup.
- **Structured model responses.** Claude returns a schema-constrained object containing `answer`, `response_type`, and stable `source_ids`. The application validates those IDs against `facts.json` before display.
- **Specific evidence.** Citations point to records such as `PROJ-FP`, `WH-RR`, or `PERS-01`, not broad sections such as “projects.”
- **Answer selection rules.** The prompt tells the model to answer directly, use the smallest useful evidence set, choose one relevant behavioral story, and avoid reciting the full resume.
- **Controlled disclosure.** The contact email and sensitive answers are used only when directly requested. Supported personal interests can be answered, while unlisted preferences are not inferred.
- **Single provider seam.** `llm_client.py` is the only module that imports `anthropic`.

## Stack

- Python 3.13
- Streamlit 1.59.2
- Anthropic Python SDK 0.116.0
- pytest 8.4.2 for development only

## Run locally

```bash
python -m venv venv
```

Activate the environment:

```bash
# macOS / Linux
source venv/bin/activate

# Windows PowerShell
venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements-dev.txt
```

Provide an API key using either an environment variable:

```bash
export ANTHROPIC_API_KEY="sk-ant-..."
```

or `.streamlit/secrets.toml`:

```toml
ANTHROPIC_API_KEY = "sk-ant-..."
```

Then run:

```bash
streamlit run app.py
```

The model can be changed without editing code:

```bash
export ANTHROPIC_MODEL="claude-haiku-4-5-20251001"
```

## Testing

Run the free local suite:

```bash
pytest -q
```

The local and GitHub Actions suites use mocked provider responses and do not make Anthropic API calls.

The suite checks:

- fact IDs, skill evidence, and FloorPlan public/private wording
- prompt boundary language and answer-selection rules
- structured-response schema and source validation
- Anthropic request construction
- evaluation-suite coverage
- Streamlit startup with and without a configured key

Run the live behavioral evaluation only when an API key is available:

```bash
EVAL_REPEATS=1 python eval_honesty.py
```

The default is three runs per case:

```bash
python eval_honesty.py
```

The current evaluation contains 29 cases across grounding, answer quality, multi-turn conversation, and boundaries. A one-pass production evaluation completed on July 13, 2026 with 29/29 passing. Three repetitions produce 87 model calls and have not been run for the current version. A previous 24/24 result belongs to the retired citation-tag architecture.

## Important files

- `facts.json` — verified source material and disclosure policies
- `prompt_builder.py` — system prompt and response instructions
- `response_model.py` — response schema, fact index, and validation
- `llm_client.py` — Anthropic API call
- `app.py` — Streamlit UI and session handling
- `eval_honesty.py` — live behavioral evaluation
- `pages/1_How_I_Built_This.py` — architecture case study page
- `BUILD_MAP.md` — current architecture specification
- `BUILD_LOG.md` — chronological implementation history

## Current verification status

The current project passes 25 deterministic unit and Streamlit smoke tests. A paid one-pass live evaluation passed 29/29 on July 13, 2026. GitHub Actions runs only the free mocked suite; live evaluation remains manual and opt-in.
