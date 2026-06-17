"""Main resume parser orchestrating extraction and field parsing."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Sequence, Union

from resumeminer.extractors.pdf import PDFExtractor
from resumeminer.parsers.contact import extract_email, extract_phone
from resumeminer.parsers.links import extract_github, extract_linkedin, extract_portfolio
from resumeminer.parsers.skills import extract_skills, load_default_skills

PathLike = Union[str, Path]

ParseResult = dict[str, Any]


def empty_result() -> ParseResult:
    """Return an empty parse result with the expected structure."""
    return {
        "email": None,
        "phone": None,
        "links": {
            "linkedin": None,
            "github": None,
            "portfolio": None,
        },
        "skills": [],
        "raw_text": "",
    }


class ResumeParser:
    """Parse structured information from a PDF resume."""

    def __init__(
        self,
        file_path: PathLike,
        skills: Sequence[str] | None = None,
    ) -> None:
        """Initialize the parser.

        Args:
            file_path: Path to the PDF resume file.
            skills: Optional custom skills list for matching.
        """
        self.file_path = Path(file_path)
        self.skills = list(skills) if skills is not None else load_default_skills()
        self._extractor = PDFExtractor()

    def parse(self) -> ParseResult:
        """Extract and parse structured data from the resume."""
        result = empty_result()

        raw_text = self._extractor.extract(self.file_path)
        result["raw_text"] = raw_text

        if not raw_text:
            return result

        result["email"] = extract_email(raw_text)
        result["phone"] = extract_phone(raw_text)
        result["links"]["linkedin"] = extract_linkedin(raw_text)
        result["links"]["github"] = extract_github(raw_text)
        result["links"]["portfolio"] = extract_portfolio(raw_text)
        result["skills"] = extract_skills(raw_text, self.skills)

        return result


def parse_resume(
    file_path: PathLike,
    skills: Sequence[str] | None = None,
) -> ParseResult:
    """Parse a PDF resume and return structured data.

    Args:
        file_path: Path to the PDF resume file.
        skills: Optional custom skills list for matching.

    Returns:
        Dictionary with email, phone, links, skills, and raw_text.
    """
    return ResumeParser(file_path, skills=skills).parse()
