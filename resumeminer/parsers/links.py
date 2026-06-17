"""URL and profile link extraction from resume text."""

from __future__ import annotations

import re

LINKEDIN_PATTERN = re.compile(
    r"(?:https?://)?(?:www\.)?linkedin\.com/in/[\w\-_%]+/?",
    re.IGNORECASE,
)

GITHUB_PATTERN = re.compile(
    r"(?:https?://)?(?:www\.)?github\.com/[\w\-]+/?",
    re.IGNORECASE,
)

PORTFOLIO_PATTERN = re.compile(
    r"(?:https?://)?(?:www\.)?[a-zA-Z0-9][-a-zA-Z0-9.]*\.[a-zA-Z]{2,}(?:/[\w\-./?#=&%+]*)?",
    re.IGNORECASE,
)

EXCLUDED_PORTFOLIO_DOMAINS = (
    "linkedin.com",
    "github.com",
    "gmail.com",
    "yahoo.com",
    "hotmail.com",
    "outlook.com",
)

EMAIL_AT_PATTERN = re.compile(r"[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}")


def _normalize_url(url: str) -> str:
    """Ensure URL has a scheme."""
    url = url.rstrip(".,)")
    if not url.lower().startswith(("http://", "https://")):
        return f"https://{url}"
    return url


def extract_linkedin(text: str) -> str | None:
    """Extract a LinkedIn profile URL from text."""
    if not text:
        return None

    match = LINKEDIN_PATTERN.search(text)
    if match is None:
        return None

    return _normalize_url(match.group(0))


def extract_github(text: str) -> str | None:
    """Extract a GitHub profile URL from text."""
    if not text:
        return None

    match = GITHUB_PATTERN.search(text)
    if match is None:
        return None

    return _normalize_url(match.group(0))


def _is_email_domain_match(text: str, start: int, end: int) -> bool:
    """Return True if the matched URL is part of an email address."""
    if start > 0 and text[start - 1] == "@":
        return True
    return bool(EMAIL_AT_PATTERN.search(text[max(0, start - 64) : end + 1]))


def extract_portfolio(text: str) -> str | None:
    """Extract a personal website or portfolio URL from text."""
    if not text:
        return None

    for match in PORTFOLIO_PATTERN.finditer(text):
        url = _normalize_url(match.group(0))
        domain = url.lower().split("//", 1)[-1]
        if any(excluded in domain for excluded in EXCLUDED_PORTFOLIO_DOMAINS):
            continue
        if _is_email_domain_match(text, match.start(), match.end()):
            continue
        return url

    return None
