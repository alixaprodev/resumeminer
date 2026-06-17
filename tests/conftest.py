"""Shared test fixtures and helpers."""

from __future__ import annotations

from pathlib import Path

import pytest
from pypdf import PdfWriter


def create_pdf_with_text(path: Path, text: str) -> None:
    """Create a simple PDF file containing the given text."""
    single_line = " ".join(text.split())
    escaped = (
        single_line.replace("\\", "\\\\")
        .replace("(", "\\(")
        .replace(")", "\\)")
    )
    stream = f"BT /F1 10 Tf 72 720 Td ({escaped}) Tj ET"
    stream_bytes = stream.encode("latin-1", errors="replace")

    objects = [
        b"1 0 obj<</Type/Catalog/Pages 2 0 R>>endobj\n",
        b"2 0 obj<</Type/Pages/Kids[3 0 R]/Count 1>>endobj\n",
        b"3 0 obj<</Type/Page/MediaBox[0 0 612 792]/Parent 2 0 R"
        b"/Resources<</Font<</F1 4 0 R>>>>/Contents 5 0 R>>endobj\n",
        b"4 0 obj<</Type/Font/Subtype/Type1/BaseFont/Helvetica>>endobj\n",
        (
            f"5 0 obj<</Length {len(stream_bytes)}>>stream\n".encode("ascii")
            + stream_bytes
            + b"\nendstream\nendobj\n"
        ),
    ]

    pdf = bytearray(b"%PDF-1.4\n")
    offsets = [0]
    for obj in objects:
        offsets.append(len(pdf))
        pdf.extend(obj)

    xref_start = len(pdf)
    pdf.extend(f"xref\n0 {len(offsets)}\n".encode("ascii"))
    pdf.extend(b"0000000000 65535 f \n")
    for offset in offsets[1:]:
        pdf.extend(f"{offset:010d} 00000 n \n".encode("ascii"))

    pdf.extend(
        f"trailer<</Size {len(offsets)}/Root 1 0 R>>\n"
        f"startxref\n{xref_start}\n%%EOF\n".encode("ascii")
    )
    path.write_bytes(pdf)


@pytest.fixture
def sample_resume_text() -> str:
    """Representative resume text for parser unit tests."""
    return """
    Jane Developer
    jane.developer@example.com
    +1 (555) 123-4567

    Skills: Python, Django, React, Docker, AWS

    https://linkedin.com/in/jane-developer
    https://github.com/janedev
    https://janedeveloper.dev

    Experience building web applications with FastAPI and PostgreSQL.
    """


@pytest.fixture
def sample_pdf(tmp_path: Path, sample_resume_text: str) -> Path:
    """Create a temporary PDF resume for integration tests."""
    pdf_path = tmp_path / "resume.pdf"
    create_pdf_with_text(pdf_path, sample_resume_text)
    return pdf_path


@pytest.fixture
def empty_pdf(tmp_path: Path) -> Path:
    """Create an empty PDF with no extractable text."""
    pdf_path = tmp_path / "empty.pdf"
    writer = PdfWriter()
    writer.add_blank_page(width=612, height=792)
    with pdf_path.open("wb") as file:
        writer.write(file)
    return pdf_path
