"""Tests for PDF text extraction."""

from __future__ import annotations

from pathlib import Path

import pytest

from resumeminer.extractors.pdf import PDFExtractionError, PDFExtractor, extract_text_from_pdf
from tests.conftest import create_pdf_with_text


def test_extract_text_from_pdf_returns_text(sample_pdf: Path, sample_resume_text: str) -> None:
    text = extract_text_from_pdf(sample_pdf)
    assert "jane.developer@example.com" in text
    assert "Python" in text


def test_extract_text_from_empty_pdf(empty_pdf: Path) -> None:
    text = extract_text_from_pdf(empty_pdf)
    assert text == ""


def test_extract_text_file_not_found() -> None:
    with pytest.raises(FileNotFoundError):
        extract_text_from_pdf("/nonexistent/resume.pdf")


def test_extract_text_invalid_extension(tmp_path: Path) -> None:
    file_path = tmp_path / "resume.txt"
    file_path.write_text("not a pdf", encoding="utf-8")

    with pytest.raises(PDFExtractionError, match="Expected a PDF file"):
        extract_text_from_pdf(file_path)


def test_extract_text_corrupted_pdf(tmp_path: Path) -> None:
    file_path = tmp_path / "bad.pdf"
    file_path.write_bytes(b"not a real pdf")

    with pytest.raises(PDFExtractionError, match="Failed to read PDF"):
        extract_text_from_pdf(file_path)


def test_pdf_extractor_class(tmp_path: Path) -> None:
    pdf_path = tmp_path / "resume.pdf"
    create_pdf_with_text(pdf_path, "Contact: test@example.com")

    extractor = PDFExtractor()
    text = extractor.extract(pdf_path)
    assert "test@example.com" in text
