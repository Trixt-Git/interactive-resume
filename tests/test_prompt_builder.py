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


def test_prompt_requires_unscripted_but_unambiguous_denials():
    text = prompt()
    # Denials are phrased naturally, but the prompt must still demand an
    # explicit negative and forbid hedging.
    assert "denial in your own words" in text
    assert '"won\'t claim"' in text
    assert "never hedge" in text
    assert "not accurate" in text
    assert "verified background" in text
    # The old word-for-word scripts must stay gone; they made every refusal
    # sound identical.
    assert "No, I haven't used that, and I don't claim it." not in text
    assert "I haven't worked with that, so I won't claim it." not in text


def test_prompt_keeps_sensitive_responses_verbatim_and_allows_pleasantries():
    text = prompt()
    assert "Use the stored response verbatim" in text
    assert "disclosure control" in text
    assert "pleasantries" in text


def test_prompt_keeps_the_voice_guide():
    # The v1 voice guide was silently flattened once during the structured-
    # output rewrite; these anchors keep its load-bearing pieces from
    # disappearing again.
    text = prompt()
    assert "not a resume reading itself aloud" in text
    assert "don't write in a monotone" in text
    assert "No cheerleader energy" in text
    assert "Honesty always outranks voice" in text


def test_prompt_varies_offtopic_redirects_instead_of_one_script():
    text = prompt()
    assert "Vary the phrasing between redirects" in text
    assert '"verified background"' in text


def test_prompt_contains_current_linkedin_and_not_rehire_language():
    text = prompt()
    assert "https://www.linkedin.com/in/wil-uhlir/" in text
    assert "rehire eligible" not in text.lower()
