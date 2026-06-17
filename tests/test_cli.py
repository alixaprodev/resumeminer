"""Tests for the command-line interface."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from resumeminer.cli import format_result, main
from tests.conftest import create_pdf_with_text


def test_format_result_shows_fields() -> None:
    output = format_result(
        {
            "email": "dev@example.com",
            "phone": "+1 555 123 4567",
            "links": {
                "linkedin": "https://linkedin.com/in/dev",
                "github": "https://github.com/dev",
                "portfolio": None,
            },
            "skills": ["Python", "Docker"],
            "raw_text": "hidden in default output",
        }
    )

    assert "dev@example.com" in output
    assert "Python, Docker" in output
    assert "raw_text" not in output


def test_cli_parse_json_output(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    pdf_path = tmp_path / "resume.pdf"
    create_pdf_with_text(
        pdf_path,
        "jane@example.com Python https://github.com/jane",
    )

    exit_code = main(["parse", str(pdf_path), "--json"])
    captured = capsys.readouterr()

    assert exit_code == 0
    payload = json.loads(captured.out)
    assert payload["email"] == "jane@example.com"
    assert "Python" in payload["skills"]
    assert payload["raw_text"]


def test_cli_parse_human_output(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    pdf_path = tmp_path / "resume.pdf"
    create_pdf_with_text(pdf_path, "jane@example.com Python")

    exit_code = main(["parse", str(pdf_path)])
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "Email:     jane@example.com" in captured.out
    assert "Skills:" in captured.out
    assert "raw_text" not in captured.out


def test_cli_missing_file(capsys: pytest.CaptureFixture[str]) -> None:
    exit_code = main(["parse", "/nonexistent/resume.pdf"])
    captured = capsys.readouterr()

    assert exit_code == 1
    assert "file not found" in captured.err.lower()


def test_cli_version_flag(capsys: pytest.CaptureFixture[str]) -> None:
    with pytest.raises(SystemExit) as exc_info:
        main(["--version"])

    assert exc_info.value.code == 0
