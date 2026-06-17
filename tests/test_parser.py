"""Tests for the main resume parser."""

from __future__ import annotations

from pathlib import Path

import pytest

from resumeminer import ResumeParser, parse_resume
from resumeminer.parser import empty_result


def test_empty_result_structure() -> None:
    result = empty_result()
    assert result["email"] is None
    assert result["phone"] is None
    assert result["links"] == {"linkedin": None, "github": None, "portfolio": None}
    assert result["skills"] == []
    assert result["raw_text"] == ""


def test_parse_resume_from_text_fields(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    pdf_path = tmp_path / "resume.pdf"
    pdf_path.write_bytes(b"%PDF-1.4\n")

    resume_text = """
    alice@example.com
    +1 555 987 6543
    https://linkedin.com/in/alice
    https://github.com/alice
    https://alice.io
    Skills: Python, AWS
    """

    monkeypatch.setattr(
        "resumeminer.parser.PDFExtractor.extract",
        lambda self, path: resume_text,
    )

    result = parse_resume(pdf_path)

    assert result["email"] == "alice@example.com"
    assert result["phone"] is not None
    assert result["links"]["linkedin"] == "https://linkedin.com/in/alice"
    assert result["links"]["github"] == "https://github.com/alice"
    assert result["links"]["portfolio"] == "https://alice.io"
    assert result["skills"] == ["Python", "AWS"]
    assert "alice@example.com" in result["raw_text"]


def test_resume_parser_custom_skills(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    pdf_path = tmp_path / "resume.pdf"
    pdf_path.touch()

    monkeypatch.setattr(
        "resumeminer.parser.PDFExtractor.extract",
        lambda self, path: "Experience with Rust and Zig.",
    )

    parser = ResumeParser(pdf_path, skills=["Rust", "Zig"])
    result = parser.parse()

    assert result["skills"] == ["Rust", "Zig"]


def test_parse_empty_pdf_returns_empty_fields(empty_pdf: Path) -> None:
    result = parse_resume(empty_pdf)
    assert result["email"] is None
    assert result["phone"] is None
    assert result["skills"] == []
    assert result["raw_text"] == ""
