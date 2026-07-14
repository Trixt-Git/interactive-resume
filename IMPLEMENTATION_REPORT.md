# WilOS v2 Implementation and Verification Report

## Implemented

- Refined production facts with corrected employment details and public/private FloorPlan language.
- Stable fact-ID indexing and duplicate detection.
- Schema-constrained Claude responses with five response types.
- Exact source validation and human-readable source labels.
- Direct-answer, role-fit, behavioral-story, and disclosure rules.
- Supported personal-interest answers with boundaries around unlisted preferences.
- Configurable model through `ANTHROPIC_MODEL`.
- Expanded live evaluation with grounding, answer-quality, conversation, and boundary suites.
- Updated Streamlit app, architecture page, README, build specification, and developer instructions.

## Verification through 2026-07-14

### Clean environment

A clean virtual environment was populated from the development dependencies.

- dependency check: no broken requirements
- pytest: 25 passed
- Python compilation: passed

### Streamlit

- server startup: passed
- `/_stcore/health`: returned `ok`
- landing-page AppTest with an environment API key: passed
- architecture-page AppTest: passed
- quick-action conversation with a mocked structured model reply: passed
- exact source marker rendering: passed
- missing-secrets configuration path: passed after fixing one discovered bug

### Anthropic SDK contract

The installed pinned SDK exposes `output_config`, and its JSON output format accepts the `type: json_schema` and `schema` fields used by `llm_client.py`.

## Bug found during testing

The initial revision called:

```python
st.secrets.get("ANTHROPIC_API_KEY", "")
```

When no secrets file existed, Streamlit raised `StreamlitSecretNotFoundError` before the intended user-facing message could render. The application now checks `ANTHROPIC_API_KEY` in the environment first and catches the missing-secrets exception before showing:

```text
API key not configured. See README.
```

A regression test now covers both missing-key and environment-key startup.

## Live evaluation

A paid one-pass live evaluation (`EVAL_REPEATS=1`) passed 29/29 on July 13, 2026: grounding 8/8, answer quality 5/5, boundaries 13/13, and conversation 3/3. The older 24/24 result was produced by the retired citation-tag architecture.

Run a development pass with:

```bash
EVAL_REPEATS=1 python eval_honesty.py
```

The default three-repeat gate has not been run for the current version because it makes 87 paid model calls. Run it only when explicitly approved:

```bash
python eval_honesty.py
```
