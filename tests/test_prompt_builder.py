from pathlib import Path

from prompt_builder import build_system_prompt, load_facts

ROOT = Path(__file__).resolve().parents[1]


def prompt():
    return build_system_prompt(load_facts(ROOT / "facts.json"))


def test_prompt_uses_wilos_name_and_structured_response_contract():
    text = prompt()
    assert "You are WilOS" in text
    assert "response_type: grounded, unsupported, sensitive, identity, or off_topic" in text
    assert "source_ids" in text
    assert "[[SOURCES:" not in text


def test_prompt_answers_supported_personal_questions_but_not_inferred_preferences():
    text = prompt()
    assert "Personal questions are answerable when personal contains the answer" in text
    assert "Do not infer unlisted preferences" in text
    assert "Are you into hockey?" not in text  # examples stay general; facts supply the actual interest


def test_prompt_has_answer_selection_rules():
    text = prompt()
    assert "Answer the actual question in the first sentence" in text
    assert "Do not recite the full resume" in text
    assert "choose one story" in text
    assert "Do not end with a generic invitation" in text


def test_prompt_preserves_locked_boundary_sentences():
    text = prompt()
    assert "No, I haven't used that, and I don't claim it." in text
    assert "I haven't worked with that, so I won't claim it." in text
    assert "That's not accurate. I haven't done that, and I won't claim it." in text
    assert "I can't do that. I only answer from Wil's verified background." in text


def test_prompt_contains_current_linkedin_and_not_rehire_language():
    text = prompt()
    assert "https://www.linkedin.com/in/wil-uhlir/" in text
    assert "rehire eligible" not in text.lower()
