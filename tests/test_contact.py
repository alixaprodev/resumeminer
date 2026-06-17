"""Tests for contact information extraction."""

from __future__ import annotations

from resumeminer.parsers.contact import extract_email, extract_phone


def test_extract_email_finds_address() -> None:
    text = "Reach me at Jane.Doe@Example.COM for details."
    assert extract_email(text) == "jane.doe@example.com"


def test_extract_email_returns_none_when_missing() -> None:
    assert extract_email("No contact details here.") is None


def test_extract_email_returns_first_match() -> None:
    text = "first@example.com and second@example.com"
    assert extract_email(text) == "first@example.com"


def test_extract_phone_finds_us_number() -> None:
    text = "Phone: +1 (555) 123-4567"
    assert extract_phone(text) == "+1 (555) 123-4567"


def test_extract_phone_finds_international_number() -> None:
    text = "Mobile: +92 300 1234567"
    phone = extract_phone(text)
    assert phone is not None
    assert "300" in phone


def test_extract_phone_returns_none_when_missing() -> None:
    assert extract_phone("No phone listed.") is None


def test_extract_phone_ignores_short_digit_sequences() -> None:
    assert extract_phone("Room 123, Building 45") is None
