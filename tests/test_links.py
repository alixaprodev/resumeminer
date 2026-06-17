"""Tests for link extraction."""

from __future__ import annotations

from resumeminer.parsers.links import extract_github, extract_linkedin, extract_portfolio


def test_extract_linkedin_with_https() -> None:
    text = "Profile: https://www.linkedin.com/in/jane-developer"
    assert extract_linkedin(text) == "https://www.linkedin.com/in/jane-developer"


def test_extract_linkedin_without_scheme() -> None:
    text = "linkedin.com/in/janedev"
    assert extract_linkedin(text) == "https://linkedin.com/in/janedev"


def test_extract_linkedin_returns_none_when_missing() -> None:
    assert extract_linkedin("No social links.") is None


def test_extract_github_with_https() -> None:
    text = "Code: https://github.com/janedev"
    assert extract_github(text) == "https://github.com/janedev"


def test_extract_github_without_scheme() -> None:
    text = "github.com/janedev"
    assert extract_github(text) == "https://github.com/janedev"


def test_extract_github_returns_none_when_missing() -> None:
    assert extract_github("No GitHub profile.") is None


def test_extract_portfolio_finds_personal_site() -> None:
    text = "Website: https://janedeveloper.dev/portfolio"
    assert extract_portfolio(text) == "https://janedeveloper.dev/portfolio"


def test_extract_portfolio_skips_linkedin_and_github() -> None:
    text = """
    https://linkedin.com/in/jane
    https://github.com/jane
    https://jane.dev
    """
    assert extract_portfolio(text) == "https://jane.dev"


def test_extract_portfolio_returns_none_when_missing() -> None:
    assert extract_portfolio("No website listed.") is None
