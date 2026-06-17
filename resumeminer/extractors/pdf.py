"""PDF text extraction using pypdf."""

from __future__ import annotations

from pathlib import Path
from typing import Union

from pypdf import PdfReader
from pypdf.errors import PdfReadError

PathLike = Union[str, Path]


class PDFExtractionError(Exception):
    """Raised when PDF text extraction fails."""


def _normalize_text(text: str) -> str:
    """Collapse excessive whitespace while preserving line breaks."""
    lines = [line.strip() for line in text.splitlines()]
    cleaned = "\n".join(line for line in lines if line)
    return cleaned.strip()


def extract_text_from_pdf(file_path: PathLike) -> str:
    """Extract text from all pages of a PDF file.

    Args:
        file_path: Path to the PDF file.

    Returns:
        Extracted and cleaned text, or an empty string if no text is found.

    Raises:
        FileNotFoundError: If the file does not exist.
        PDFExtractionError: If the PDF cannot be read or parsed.
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"PDF file not found: {path}")

    if path.suffix.lower() != ".pdf":
        raise PDFExtractionError(f"Expected a PDF file, got: {path.suffix}")

    try:
        reader = PdfReader(str(path))
    except PdfReadError as exc:
        raise PDFExtractionError(f"Failed to read PDF: {path}") from exc
    except Exception as exc:
        raise PDFExtractionError(f"Failed to open PDF: {path}") from exc

    if reader.is_encrypted:
        try:
            reader.decrypt("")
        except Exception as exc:
            raise PDFExtractionError(f"PDF is encrypted and cannot be read: {path}") from exc

    page_texts: list[str] = []
    for page in reader.pages:
        try:
            page_text = page.extract_text() or ""
        except Exception:
            page_text = ""
        if page_text.strip():
            page_texts.append(page_text)

    return _normalize_text("\n".join(page_texts))


class PDFExtractor:
    """Extract text from PDF resume files."""

    def extract(self, file_path: PathLike) -> str:
        """Extract text from a PDF file."""
        return extract_text_from_pdf(file_path)
