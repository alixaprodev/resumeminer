"""Text extraction from resume files."""

from resumeminer.extractors.pdf import PDFExtractor, extract_text_from_pdf

__all__ = ["PDFExtractor", "extract_text_from_pdf"]
