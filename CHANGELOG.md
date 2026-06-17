# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-06-18

### Added

- PDF text extraction for resume files using `pypdf`
- Email and phone number extraction
- LinkedIn, GitHub, and portfolio URL extraction
- Configurable skill matching with a bundled default skills list
- `ResumeParser` class and `parse_resume()` convenience function
- CLI: `resumeminer parse <file>` with human-readable and `--json` output
- Python 3.9+ support

[0.1.0]: https://github.com/alixaprodev/resumeminer/releases/tag/v0.1.0
