# Build Log

A chronological record of what was actually built and changed, with commit
hashes for traceability. This complements `BUILD_MAP.md` — that document is the
plan (the locked, up-front specification); this one is the history of execution
against it, plus the refinement work that came after the initial build.

Design decisions and their rationale live in the code and in each commit
message; this log is the map from "what changed" to "which commit." For the
locked spec and its own amendment log (v1.1–v1.9, covering the honesty-rule
evolution), see `BUILD_MAP.md`.

---

## Initial build — 2026-07-08

The app was built phase-by-phase against `BUILD_MAP.md`, starting from the
Streamlit template scaffold.

| Commit | Change |
|--------|--------|
| `a77e643` | Initial commit (scaffold) |
| `ad334da` | Replace Streamlit template scaffolding with the Ask Wil app |
| `2b4a218` | Add `streamlit_app.py` shim for Streamlit Cloud's fixed entry point |
| `8dc2859` | Add distilled voice guide as a VOICE section in the system prompt |
| `3ea5ada` | Style pass: Fidelity-green theme, refusal marker, streaming |
| `f8b570b` | Add 4 additive UX features: starters, opening message, fact citations, case-study page |
| `9bad56e` | Reorder starters: lead with strengths, rehire question last |
| `a60a53b` | Update question for Fidelity's LEAP role |
| `9f7c8d7`, `9bec5ee`, `3ab64ca` | Copy/label fixes on the starter buttons |
| `1e5fe94` | Refactor CSS styles and update color palette |
| `b3f69ac` | Rebrand to WilOS, category-based conversation starters |
| `2038873` | Merge refined WilOS style as canonical `style.py` |
| `6cbe9c3` | Change landing tagline to "Ready when you are." |
| `6c744c7` | Center landing page like a ChatGPT/Claude homepage |

## Refinement work — 2026-07-08 → 2026-07-09

Post-build iteration on facts accuracy, conversation UX, honesty behavior, and
visual design.

### Content

| Commit | Change |
|--------|--------|
| `9bd9b41` | Update FloorPlan facts to reflect the project's actual scope (decision-support app, OEE analysis, plant-leadership adoption) rather than a press-floor scheduler |

### Conversation UX & layout

| Commit | Change |
|--------|--------|
| `7aa4a6a` | Tighten hero layout: smaller title, shorter hero, narrower container |
| `bebdc5f` | Move chat input inline into the hero (ChatGPT-style), not pinned to the page bottom |
| `b9378cc` | Rerun after the first exchange to drop the hero immediately |
| `4c2c817` | Keep quick-action buttons in a persistent bottom bar; stop forcing a rerun |
| `a07582b` | Switch to chat mode immediately on submit, before the reply streams in (pending-input pattern) |
| `a45a0ef` | Refactor layout for a focused recruiter tool: minimal toolbar, styled sidebar nav, bordered chat panel |
| `3abf9d4` | Fix: render the bottom bar before the chat panel so the input appears during streaming, not after |

### Honesty behavior

| Commit | Change |
|--------|--------|
| `3944284` | Split casual off-topic small talk from unsupported-claim refusals — added rule 9 (cheeky redirect) while keeping the strict professional-claim refusals; eval grew from 20 → 24 cases (`BUILD_MAP.md` amendment v1.8) |
| `c96c213` | Vary rule 9's redirect across six approved styles (amendment v1.9) |

> **Deploy gate note:** the published eval-results block in `README.md`
> pre-dates rule 9 and reflects a 20-case run. `eval_honesty.py` is now a
> 24-case suite and must be run for real (it costs live API calls, run
> manually) to confirm 24/24 before go-live. The rule-9 additions are
> structurally verified (anchors present in the built prompt, unit tests pass)
> but not yet confirmed against the live model.

### Visual design / palette

| Commit | Change |
|--------|--------|
| `94c71a6` | Restore the original Fidelity green (`#3F7623`) after a prior refactor had drifted it to a generic Material green |
| `0ee15cd` | Swap the dark-olive green for a more vivid, higher-contrast green |
| `7171ae4` | Replace the green-heavy palette with a warm graphite / slate-blue / brass system |
| `5c25156` | Restyle to the Starbucks-inspired warm café design system: cream canvas, four-tier green, gold ceremony accent, full-pill buttons, whisper-soft card lift, tight tracking |
| `293523f` | Wrap "OS" in the wordmark span so the gold accent renders |

---

*This log is maintained alongside the code. New entries are appended in
chronological order; nothing is rewritten after the fact.*

## Structured-output revision — 2026-07-13

- Promoted the refined fact record to production `facts.json`.
- Distinguished the internal FloorPlan enterprise application from the public portfolio copy.
- Added the verified LinkedIn URL and removed rehire-eligibility language.
- Reorganized skills into categories with evidence IDs; removed `applied AI/LLM tooling` as a claimed skill.
- Added behavioral-story use controls and sensitive disclosure policies.
- Replaced trailing `[[SOURCES: ...]]` prose with schema-constrained model output.
- Added `response_model.py` for fact indexing, schema construction, and semantic validation.
- Replaced broad source sections with exact stable fact IDs.
- Updated the prompt to answer supported personal questions and refuse only unlisted preferences.
- Added answer-selection rules for direct answers, role-fit synthesis, and one-story behavioral responses.
- Expanded the live evaluation to 29 cases across four suites, including multi-turn tests.
- Added Streamlit startup tests.
- Testing exposed a missing-secrets failure: `st.secrets.get()` raised before the intended configuration message when no secrets file existed. Fixed by checking the environment first and handling `StreamlitSecretNotFoundError`.
- Reconciled README, BUILD_MAP, CLAUDE instructions, and the architecture page with the structured-output implementation.

## Production hardening and UI refinement — 2026-07-13 to 2026-07-14

- Published WilOS at `https://wilresume.streamlit.app/` from `main`.
- Completed a paid one-pass behavioral evaluation with 29/29 cases passing.
- Fixed broad career answers being rejected when they contained more than four valid source IDs.
- Added explicit provider timeouts, controlled retry behavior, and flushed request-error logging.
- Replaced long inline source lists with a compact expandable verified-source marker.
- Refined landing and active-chat guidance, wordmark sizing, and assistant-label casing.
- Refined the current-role analytics narrative and required broad career answers to mention the in-progress master's program.
- Removed the phone number from the public fact corpus and contact responses.
- Split production and development dependencies, pinned deployed versions, and added free mocked GitHub Actions tests.

## Naturalness revision — 2026-07-15

- Replaced the word-for-word boundary denial scripts with a behavioral contract: denials must open with an explicit negative and never hedge, but the phrasing is the model's own so repeated refusals stop sounding identical. Sensitive stored responses and the out-of-scope response remain verbatim as disclosure controls.
- Added a pleasantry carve-out: greetings, thanks, and goodbyes get one brief natural sentence classified `off_topic` with no sources, instead of the stored out-of-scope script.
- Added follow-up continuity to the answer strategy: follow-ups continue the conversation instead of re-introducing established context, and may open with "Yes —" or "No —".
- Rewrote the voice guidance to require contractions, varied sentence openings, and yes/no-first answers; rewrote the refusal few-shot examples in looser phrasing and added a multi-turn FloorPlan example and a pleasantry example.
- Rewrote the out-of-scope response in `facts.json` with contractions while keeping the "outside my verified background" evaluation anchor.
- Raised sampling temperature from 0.2 to 0.5 for looser phrasing; the schema, semantic validation, and eval anchors carry the grounding guarantees.
- Broadened the unsupported-claim eval anchors into a shared `DENIAL_MARKERS` set and added a `pleasantry_close` conversation case (30 cases, 90 calls per full run). The 29/29 July 13 score predates this revision; a fresh live run is required before publishing a new score.
- Rebuilt the How I Built This page: leads with the failure a naive resume bot exhibits, shows a real refusal exchange with its source label, gives prompt injection its own section, reports live suite counts imported from `eval_honesty.py`, explains prompt caching, and ends with "try to break it" prompts. Avoided `st.page_link` because the local and deployed entrypoints register different main pages.
- Updated prompt tests for the unscripted-denial contract and added a smoke test for the How I Built This page.

## Voice guide restoration — 2026-07-15

- Found that the v2.0 structured-output rewrite had flattened the v1 voice guide: the rhythm, tactile-word, no-cheerleader-energy, mechanical-metaphor, and honesty-outranks-voice guidance was reduced to one short paragraph, and the v1.9 six-style casual redirects collapsed back into a single stock out-of-scope sentence — the exact repetitiveness v1.9 existed to fix.
- Restored the full voice guide into the VOICE section, merged with the newer contraction/yes-no-first/follow-up rules.
- Replaced the verbatim out-of-scope script with a varied self-aware redirect in the model's own words, anchored on the phrase "verified background" so the evaluation stays checkable. Stored sensitive responses remain the only verbatim category. Added a second off-topic few-shot example to demonstrate variation.
- Loosened the four off-topic eval anchors from the full stock sentence to the "verified background" anchor.
- Added prompt regression tests that pin the voice-guide anchors and the vary-redirects instruction, so the guide cannot be silently dropped in a future rewrite again.
- Updated BUILD_MAP and the How I Built This page to match. A fresh live eval run is still required before publishing a new behavioral score.

## Response reveal animation — 2026-07-15

- Replaced the instant full-answer render with a word-by-word reveal via `st.write_stream` (`reveal_answer` generator in `WilOS.py`), so responses type out naturally instead of a spinner resolving into a wall of text.
- The reveal is presentational only: `get_reply` still returns a complete, schema-validated reply before the first word appears, preserving the "validate before rendering anything" guarantee. Considered and rejected true token streaming from the provider, because schema-constrained JSON cannot be safely displayed or source-validated mid-stream.
- Only the fresh pending reply animates; history re-renders continue to use `st.write` and do not re-animate on rerun.
- Updated the How I Built This tradeoffs section and BUILD_MAP UI notes to describe the simulated reveal and why streaming raw output is avoided.

## Employer-neutral generalization — 2026-07-20

- Generalized the fact corpus for use across all job applications instead of a single targeted employer.
- Removed `career_target.immediate_focus` (Fidelity Investments LEAP Program, Systems Analyst track); the generic `career_target.text` systems-analyst statement stands on its own.
- Reworded the `why_left_fidelity` stored sensitive response to drop the applying-back framing ("grow there long term") in favor of employer-neutral phrasing, and updated the matching `exact_answer` in `eval_honesty.py`. The disclosure control and stable ID `ST-FID` are unchanged.
- Fidelity remains in `work_history` (`WH-FID`) as verified employment history; no facts were removed or invented.

## Recruiter-side landing revisions — 2026-07-20

- Replaced the role-specific quick actions ("Systems", "Role Fit" — the latter hardcoded a systems analyst framing) with role-neutral ones: "Career Change" (Why the career change?) and "Stump Me" (What can't you do?). The bot now names its own career target instead of the button presuming the recruiter's req, and the stump-me button surfaces the anti-fabrication behavior — the app's differentiator — on the landing page instead of leaving it buried in How I Built This.
- Added a hero tagline stating the trust contract up front: every answer is backed by the verified background, including what I can't do. Visitors arrive from the resume already knowing who Wil is; the landing page's job is to explain what this app is and why to trust it.
- Added a small "Connect with Wil on LinkedIn" footer link to the hero and the chat bottom bar, covering the forwarded-link case where the viewer never saw the resume. No email is shown, preserving the contact-disclosure policy.
- Updated the smoke test's expected button labels.

## Recruiter screen facts and multi-role career target — 2026-07-20

- Broadened `career_target.text` (TGT-01) from systems-analyst-specific phrasing to multiple technology roles anchored on the same evidenced strengths, since the link now goes out with applications across role types. The bot names its own target; the UI no longer presumes the viewer's req.
- Added a `logistics` record (LOG-01) with owner-confirmed screen answers: open to on-site/hybrid/remote, Raleigh/Triangle or remote only (no relocation), US work authorization with no sponsorship needed, two weeks' notice with start-date flexibility. Answered directly when asked, never volunteered — same discipline as the sensitive-topics policy.
- Added two live eval cases (`relocation`, `work_authorization`) pinning LOG-01 grounding, bringing the suite to 32 cases. A fresh live run is required before publishing a new score.

## Authenticity pass on the voice — 2026-07-20

- Added an "answering on the spot" clause to the VOICE guide: vary answer shape instead of repeating the same tidy three-part structure, allow occasional fragments and dash-asides, prefer concrete numbers to adjectives, and drop the stated moral when the result makes the point. All pinned voice-guide anchors unchanged.
- Loosened the two most pre-written-sounding few-shot examples: the develop-someone story no longer ends in a packaged lesson sentence, and the role-fit answer trades parallel clauses for a blunter close. Both remain fully fact-supported.
- Added a "Why the career change?" few-shot — the new landing quick action had no example guiding it. Grounded in NAR-01, PROJ-FP, EDU-01, with the POS-reporting line supported by WH-MYB's independent-reporting highlight.
