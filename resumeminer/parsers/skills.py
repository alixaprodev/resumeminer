"""Skills extraction using configurable skill dictionaries."""

from __future__ import annotations

import re
from importlib import resources
from typing import Sequence


def load_default_skills() -> list[str]:
    """Load the default skills list from the bundled data file."""
    skills_file = resources.files("resumeminer.data").joinpath("skills.txt")
    content = skills_file.read_text(encoding="utf-8")
    return [line.strip() for line in content.splitlines() if line.strip()]


def _skill_pattern(skill: str) -> re.Pattern[str]:
    """Build a case-insensitive word-boundary pattern for a skill."""
    escaped = re.escape(skill)
    if skill.endswith(".js"):
        escaped = escaped.replace(r"\.js", r"\.?js")
    return re.compile(rf"(?<![A-Za-z0-9.]){escaped}(?![A-Za-z0-9])", re.IGNORECASE)


def extract_skills(text: str, skills: Sequence[str] | None = None) -> list[str]:
    """Extract skills from text using case-insensitive matching.

    Args:
        text: Resume text to search.
        skills: Optional custom skills list. Uses defaults when not provided.

    Returns:
        Deduplicated list of matched skills with readable names preserved.
    """
    if not text:
        return []

    skill_list = list(skills) if skills is not None else load_default_skills()
    matched: list[str] = []
    seen_lower: set[str] = set()

    for skill in skill_list:
        if not skill:
            continue
        if _skill_pattern(skill).search(text) is None:
            continue
        key = skill.lower()
        if key in seen_lower:
            continue
        seen_lower.add(key)
        matched.append(skill)

    return matched
