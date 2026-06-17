"""A lightweight Python library for extracting structured information from PDF resumes."""

from resumeminer.parser import ResumeParser, parse_resume

__all__ = ["ResumeParser", "parse_resume", "__version__"]
__version__ = "0.1.0"
