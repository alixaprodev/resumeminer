"""Contact information extraction from resume text."""

from __future__ import annotations

import re

EMAIL_PATTERN = re.compile(
    r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
)

PHONE_PATTERN = re.compile(
    r"""
    (?:
        (?:\+?\d{1,3}[\s.-]?)?              # optional country code
        (?:\(?\d{2,4}\)?[\s.-]?)?           # optional area code
        (?:\d[\s.-]?){6,14}\d               # remaining digits with separators
    )
    """,
    re.VERBOSE,
)


def extract_email(text: str) -> str | None:
    """Extract the first email address found in text."""
    if not text:
        return None

    match = EMAIL_PATTERN.search(text)
    if match is None:
        return None

    return match.group(0).lower()


def extract_phone(text: str) -> str | None:
    """Extract the best phone number match found in text."""
    if not text:
        return None

    candidates: list[str] = []
    for match in PHONE_PATTERN.finditer(text):
        phone = match.group(0).strip()
        digits = re.sub(r"\D", "", phone)
        if len(digits) < 7:
            continue
        candidates.append(re.sub(r"\s+", " ", phone))

    if not candidates:
        return None

    return max(candidates, key=lambda value: len(re.sub(r"\D", "", value)))
