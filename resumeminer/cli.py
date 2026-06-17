"""Command-line interface for ResumeMiner."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from resumeminer import __version__
from resumeminer.extractors.pdf import PDFExtractionError
from resumeminer.parser import parse_resume

ParseResult = dict[str, Any]


def build_parser() -> argparse.ArgumentParser:
    """Build the CLI argument parser."""
    parser = argparse.ArgumentParser(
        prog="resumeminer",
        description="A lightweight Python library for extracting structured information from PDF resumes.",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"resumeminer {__version__}",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    parse_cmd = subparsers.add_parser("parse", help="Parse a PDF resume")
    parse_cmd.add_argument("file", type=Path, help="Path to the PDF resume")
    parse_cmd.add_argument(
        "--json",
        action="store_true",
        help="Print full structured output as JSON (includes raw_text)",
    )

    return parser


def format_result(result: ParseResult) -> str:
    """Format parse result as human-readable text."""
    skills = ", ".join(result["skills"]) if result["skills"] else "—"
    lines = [
        f"Email:     {result['email'] or '—'}",
        f"Phone:     {result['phone'] or '—'}",
        f"LinkedIn:  {result['links']['linkedin'] or '—'}",
        f"GitHub:    {result['links']['github'] or '—'}",
        f"Portfolio: {result['links']['portfolio'] or '—'}",
        f"Skills:    {skills}",
    ]
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    """Entry point for the resumeminer CLI."""
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "parse":
        if not args.file.exists():
            print(f"Error: file not found: {args.file}", file=sys.stderr)
            return 1

        try:
            result = parse_resume(args.file)
        except PDFExtractionError as exc:
            print(f"Error: {exc}", file=sys.stderr)
            return 1
        except FileNotFoundError as exc:
            print(f"Error: {exc}", file=sys.stderr)
            return 1

        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print(format_result(result))

        return 0

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
