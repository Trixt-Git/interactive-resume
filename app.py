from __future__ import annotations

import html
import os

import streamlit as st
from streamlit.errors import StreamlitSecretNotFoundError

from llm_client import get_reply
from prompt_builder import build_system_prompt, load_facts
from response_model import LLMReply, build_fact_index
from style import STYLE

st.set_page_config(page_title="WilOS", page_icon="💬")
st.markdown(STYLE, unsafe_allow_html=True)

api_key = os.getenv("ANTHROPIC_API_KEY", "")
if not api_key:
    try:
        api_key = st.secrets.get("ANTHROPIC_API_KEY", "")
    except StreamlitSecretNotFoundError:
        api_key = ""
if not api_key:
    st.error("API key not configured. See README.")
    st.stop()

if "facts" not in st.session_state:
    st.session_state["facts"] = load_facts()
if "fact_index" not in st.session_state:
    st.session_state["fact_index"] = build_fact_index(st.session_state["facts"])
if "system_prompt" not in st.session_state:
    st.session_state["system_prompt"] = build_system_prompt(st.session_state["facts"])
if "messages" not in st.session_state:
    st.session_state["messages"] = []
if "pending_user_input" not in st.session_state:
    st.session_state["pending_user_input"] = None

is_empty = not st.session_state["messages"]

if not is_empty:
    st.markdown(
        '<div class="wilos-title wilos-title--chat">Wil<span>OS</span></div>',
        unsafe_allow_html=True,
    )


def render_marker(response_type: str, source_ids: list[str] | tuple[str, ...]) -> None:
    if response_type in {"unsupported", "off_topic"}:
        st.markdown(
            '<div class="askwil-marker askwil-marker--refusal">outside verified facts</div>',
            unsafe_allow_html=True,
        )
        if response_type == "off_topic" or not source_ids:
            return
    if response_type == "error":
        st.markdown(
            '<div class="askwil-marker askwil-marker--refusal">temporary response error</div>',
            unsafe_allow_html=True,
        )
        return

    labels = [st.session_state["fact_index"].get(source_id, source_id) for source_id in source_ids]
    if labels:
        count = len(labels)
        noun = "source" if count == 1 else "sources"
        items = "".join(f"<li>{html.escape(label)}</li>" for label in labels)
        st.markdown(
            '<details class="askwil-sources">'
            f'<summary>✓ Verified from Wil\'s background · {count} {noun}</summary>'
            f"<ul>{items}</ul>"
            "</details>",
            unsafe_allow_html=True,
        )


def render_history() -> None:
    for message in st.session_state["messages"]:
        if message["role"] == "assistant":
            with st.chat_message("assistant", avatar="💬"):
                st.markdown('<div class="askwil-label">WilOS</div>', unsafe_allow_html=True)
                st.write(message["content"])
                render_marker(message.get("response_type", "grounded"), message.get("source_ids", []))
        else:
            with st.chat_message("user"):
                st.write(message["content"])


def conversation_messages() -> list[dict]:
    recent = [
        {"role": message["role"], "content": message["content"]}
        for message in st.session_state["messages"][-12:]
    ]
    if recent and recent[0]["role"] != "user":
        recent = recent[1:]
    return recent


def render_pending_reply() -> None:
    with st.chat_message("assistant", avatar="💬"):
        st.markdown('<div class="askwil-label">WilOS</div>', unsafe_allow_html=True)
        with st.spinner("Checking the verified record..."):
            reply: LLMReply = get_reply(
                api_key,
                st.session_state["system_prompt"],
                conversation_messages(),
                set(st.session_state["fact_index"]),
            )
        st.write(reply.answer)
        render_marker(reply.response_type, reply.source_ids)

    st.session_state["messages"].append(
        {
            "role": "assistant",
            "content": reply.answer,
            "response_type": reply.response_type,
            "source_ids": list(reply.source_ids),
        }
    )
    st.session_state["pending_user_input"] = None


QUICK_ACTIONS = [
    ("Experience", "Walk me through your work experience."),
    ("Projects", "Tell me about your projects."),
    ("Systems", "How do you approach building systems and tools?"),
    ("Role Fit", "Why are you a fit for a systems analyst role?"),
]


def render_quick_actions(container, key_prefix: str):
    clicked = None
    columns = container.columns(4)
    for column, (label, prompt) in zip(columns, QUICK_ACTIONS):
        if column.button(label, key=f"{key_prefix}_{label.replace(' ', '_').lower()}"):
            clicked = prompt
    return clicked


def render_bottom_bar(key_prefix: str):
    with st.bottom:
        with st.container(key="wilos_bottom"):
            value = st.chat_input(
                "Ask about Wil's background, projects, interests, or role fit",
                key=f"{key_prefix}_chat_input",
            )
            clicked = render_quick_actions(st, key_prefix)
            return clicked or value


def submit_input(text: str) -> None:
    if len(st.session_state["messages"]) >= 60:
        st.warning(
            "This session has hit its message limit. Refresh to start a new one, "
            "or use the contact links in Wil's resume."
        )
    elif len(text) > 1000:
        st.warning("That message is too long for this bot. Please shorten it.")
    else:
        st.session_state["messages"].append({"role": "user", "content": text})
        st.session_state["pending_user_input"] = text
        st.rerun()


if is_empty:
    with st.container(key="wilos_hero"):
        st.markdown('<div class="wilos-title">Wil<span>OS</span></div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="wilos-subtitle">Ask your own question below, or choose a starting point.</div>',
            unsafe_allow_html=True,
        )
        user_input = st.chat_input(
            "Ask about Wil's background, projects, interests, or role fit",
            key="hero_chat_input",
        )
        clicked = render_quick_actions(st, "hero")
        if clicked:
            user_input = clicked
else:
    user_input = render_bottom_bar("main")

if user_input:
    submit_input(user_input)

if not is_empty:
    with st.container(key="wilos_chat_panel"):
        render_history()
        if st.session_state["pending_user_input"]:
            render_pending_reply()
