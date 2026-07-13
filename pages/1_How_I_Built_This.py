import streamlit as st

from style import STYLE

st.set_page_config(page_title="How I Built This | WilOS", page_icon="💬")
st.markdown(STYLE, unsafe_allow_html=True)

st.title("How I Built This")
st.markdown(
    "WilOS is a systems-analysis project disguised as an interactive resume. "
    "The main requirement is not to sound impressive. It is to answer usefully "
    "without inventing anything about a real candidate."
)

st.header("One complete source of truth")
st.markdown(
    """
The full verified `facts.json` file is compiled into the system prompt at startup.
There is no vector database or retrieval layer because the corpus is one person's
background. At this size, retrieval would create a new way to miss relevant facts
without solving a context-window problem.

Each citeable entry has a stable id. Skills are grouped by category and mapped to
evidence ids. Behavioral stories carry selection controls so the model knows when
a story is useful and when it should not be volunteered.
"""
)

st.header("Structured answers, not citation-shaped text")
st.markdown(
    """
The first version asked the model to append a trailing source tag and used a
regular expression to remove it before display. That worked most of the time, but
it made citation correctness another instruction-following problem.

The current version uses the provider's structured-output feature. The model must
return three fields: the visible answer, a response type, and stable source ids.
The JSON schema limits ids to values that actually exist in the facts file. The
application validates the semantics again before rendering anything.

That means the UI does not guess whether an answer was a refusal by searching for
phrases such as "haven't used." It reads an explicit `response_type`. It also shows
specific evidence such as `FloorPlan` or `Software Implementation Consultant at
Reynolds & Reynolds`, rather than a broad label such as `projects`.
"""
)

st.header("Answer selection matters as much as refusal")
st.markdown(
    """
The original prompt spent most of its attention on what the model could not say.
The revised prompt keeps those boundaries, then gives the model a decision process:
answer in the first sentence, select the smallest useful evidence set, use one
matching story for behavioral questions, and explain role fit instead of listing
keywords.

Supported personal questions are now answerable. WilOS can say that Wil follows
hockey because that fact exists. It cannot invent a favorite team because that fact
does not exist. Sensitive answers and contact details are available only when the
question directly calls for them.
"""
)

st.header("Four separate evaluation problems")
st.markdown(
    """
A single honesty score hides different failure modes, so the live evaluation is
split into four suites:

- **Grounding:** Is the answer factually supported, and are the source ids correct?
- **Answer quality:** Is it direct, concise, and based on the best story rather than a resume dump?
- **Conversation:** Do follow-up questions retain the right context without crossing a boundary?
- **Boundaries:** Does the model reject unsupported skills, false premises, prompt injection, and unlisted preferences?

The default live run executes every case three times. A single pass can show that a
prompt works once; it cannot show that the behavior is stable.
"""
)

st.header("System data flow")
st.markdown(
    """
<div class="wilos-flow">
  <div class="wilos-flow-step">User submits a question</div>
  <div class="wilos-flow-arrow">↓</div>
  <div class="wilos-flow-step">Input and session limits are checked before the API call</div>
  <div class="wilos-flow-arrow">↓</div>
  <div class="wilos-flow-step">The cached system prompt contains the full verified facts file and answer rules</div>
  <div class="wilos-flow-arrow">↓</div>
  <div class="wilos-flow-step">Claude returns schema-constrained JSON</div>
  <div class="wilos-flow-arrow">↓</div>
  <div class="wilos-flow-step">WilOS validates response type and source ids against the facts index</div>
  <div class="wilos-flow-arrow">↓</div>
  <div class="wilos-flow-step">The visible answer and specific evidence labels are rendered</div>
</div>
""",
    unsafe_allow_html=True,
)

st.header("Deliberate tradeoffs")
st.markdown(
    """
The deployed model remains configurable, with Haiku 4.5 as the default. The goal is
not to use the largest model available. It is to find the least expensive model
that consistently passes the same grounding and answer-quality tests.

The app buffers the short structured response instead of streaming raw JSON. That
trades a small amount of perceived speed for reliable parsing and a cleaner UI.
The enterprise FloorPlan application and company data remain private; only a
separate portfolio copy is public.
"""
)
