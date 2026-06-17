"""Tests for skills extraction."""

from __future__ import annotations

from resumeminer.parsers.skills import extract_skills, load_default_skills


def test_load_default_skills() -> None:
    skills = load_default_skills()
    assert "Python" in skills
    assert "Docker" in skills
    assert len(skills) == 16


def test_extract_skills_case_insensitive() -> None:
    text = "Experience with python, DJANGO, and react."
    skills = extract_skills(text)
    assert skills == ["Python", "Django", "React"]


def test_extract_skills_deduplicated() -> None:
    text = "Python python PYTHON and Docker docker"
    skills = extract_skills(text)
    assert skills.count("Python") == 1
    assert skills.count("Docker") == 1


def test_extract_skills_preserves_readable_names() -> None:
    text = "Built APIs with fastapi and node.js"
    skills = extract_skills(text)
    assert "FastAPI" in skills
    assert "Node.js" in skills


def test_extract_skills_custom_list() -> None:
    text = "Expert in Rust and Go programming."
    skills = extract_skills(text, skills=["Rust", "Go", "Python"])
    assert skills == ["Rust", "Go"]


def test_extract_skills_empty_text() -> None:
    assert extract_skills("") == []


def test_extract_skills_no_matches() -> None:
    assert extract_skills("General office administration.") == []
