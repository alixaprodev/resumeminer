"""Integration tests using real resume PDFs from tests/fixtures/."""

from __future__ import annotations

from pathlib import Path

import pytest

from resumeminer import parse_resume

FIXTURES_DIR = Path(__file__).parent / "fixtures"

REAL_RESUME_PDFS = sorted(FIXTURES_DIR.glob("*.pdf"))


@pytest.mark.parametrize("pdf_path", REAL_RESUME_PDFS, ids=lambda p: p.name)
def test_parse_real_resume_pdf(pdf_path: Path) -> None:
    """Real-world PDFs should extract text and at least an email address."""
    result = parse_resume(pdf_path)

    assert result["raw_text"], f"expected extractable text in {pdf_path.name}"
    assert result["email"], f"expected an email in {pdf_path.name}"
    assert isinstance(result["skills"], list)
    assert set(result["links"]) == {"linkedin", "github", "portfolio"}


@pytest.mark.skipif(
    not (FIXTURES_DIR / "software_engineer_resume.pdf").exists(),
    reason="software_engineer_resume.pdf fixture not downloaded",
)
def test_software_engineer_resume_extracts_links() -> None:
    """Known fixture with LinkedIn and GitHub links."""
    result = parse_resume(FIXTURES_DIR / "software_engineer_resume.pdf")

    assert result["links"]["linkedin"] == "https://linkedin.com/in/dev-amr-elsherif"
    assert result["links"]["github"] == "https://github.com/dev-amr-elsherif"
