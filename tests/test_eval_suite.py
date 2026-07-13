from eval_honesty import CASES


def test_eval_suite_covers_four_concerns():
    suites = {case.suite for case in CASES}
    assert suites == {"grounding", "answer_quality", "conversation", "boundaries"}


def test_eval_suite_includes_supported_and_unsupported_personal_questions():
    ids = {case.case_id for case in CASES}
    assert "supported_hockey" in ids
    assert "unsupported_team_preference" in ids
    assert "personal_followup_boundary" in ids


def test_eval_suite_includes_multi_turn_cases():
    assert sum(len(case.turns) > 1 for case in CASES) >= 3
