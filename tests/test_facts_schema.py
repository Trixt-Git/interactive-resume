import json
from pathlib import Path

from response_model import build_fact_index

ROOT = Path(__file__).resolve().parents[1]


def load():
    return json.loads((ROOT / "facts.json").read_text(encoding="utf-8"))


def test_fact_ids_are_unique_and_expected_core_ids_exist():
    facts = load()
    index = build_fact_index(facts)
    assert len(index) == len(set(index))
    assert {"ID-01", "NAR-01", "ROLE-01", "SKL-01", "PROJ-FP", "PROJ-WOS", "PERS-01"} <= set(index)


def test_skill_categories_are_the_canonical_whitelist():
    skills = load()["skills"]
    categorized = [item for group in skills["categories"].values() for item in group]
    assert categorized == skills["confirmed"]
    assert len(categorized) == len(set(categorized))
    assert "applied AI/LLM tooling" not in categorized


def test_skill_evidence_references_real_fact_ids():
    facts = load()
    valid_ids = set(build_fact_index(facts))
    skills = facts["skills"]
    assert set(skills["evidence"]) == set(skills["confirmed"])
    for skill, source_ids in skills["evidence"].items():
        assert source_ids, skill
        assert set(source_ids) <= valid_ids, skill


def test_floorplan_public_and_enterprise_versions_are_distinct():
    floorplan = next(project for project in load()["projects"] if project["id"] == "PROJ-FP")
    text = " ".join(floorplan["outcomes"]).lower()
    assert "enterprise version" in text
    assert "not public" in text
    assert "portfolio copy" in text


def test_sensitive_and_contact_policies_do_not_invite_volunteering():
    facts = load()
    assert "only" in facts["identity"]["contact_policy"].lower()
    assert "phone" not in facts["identity"]["contact"]
    assert "do not volunteer" in facts["sensitive_topics"]["policy"].lower()
