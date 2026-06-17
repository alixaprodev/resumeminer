# ResumeMiner

A lightweight Python library for extracting structured information from PDF resumes.

## Features

- PDF text extraction via `pypdf`
- Email and phone number extraction
- LinkedIn, GitHub, and portfolio URL extraction
- Configurable skill matching against a bundled default list
- Simple API and command-line interface
- Structured dictionary output with raw extracted text

## Installation

```bash
pip install resumeminer
```

Requires Python 3.9 or newer.

### Development

```bash
git clone https://github.com/alixaprodev/resumeminer.git
cd resumeminer
pip install -e ".[dev]"
```

## Quick Start

```python
from resumeminer import ResumeParser

parser = ResumeParser("resume.pdf")
result = parser.parse()

print(result["email"])
print(result["skills"])
```

```python
from resumeminer import parse_resume

result = parse_resume("resume.pdf")
print(result)
```

Optional custom skills list:

```python
parser = ResumeParser("resume.pdf", skills=["Python", "Rust", "Go"])
result = parser.parse()
```

## CLI Usage

Parse a resume:

```bash
resumeminer parse resume.pdf
```

Human-readable output (default):

```text
Email:     jane.developer@example.com
Phone:     +1 (555) 123-4567
LinkedIn:  https://linkedin.com/in/jane-developer
GitHub:    https://github.com/janedev
Portfolio: https://janedeveloper.dev
Skills:    Python, Django, React, Docker, AWS
```

Full JSON output (includes `raw_text`):

```bash
resumeminer parse resume.pdf --json
```

Print version:

```bash
resumeminer --version
```

## Output Example

```python
{
    "email": "jane.developer@example.com",
    "phone": "+1 (555) 123-4567",
    "links": {
        "linkedin": "https://linkedin.com/in/jane-developer",
        "github": "https://github.com/janedev",
        "portfolio": "https://janedeveloper.dev"
    },
    "skills": ["Python", "Django", "React", "Docker", "AWS"],
    "raw_text": "..."
}
```

## Supported Files

- PDF resumes with extractable text

Scanned or image-only PDFs are not supported in v0.1.0.

## Limitations

- Extraction quality depends on PDF structure and formatting
- Regex-based parsing may miss or misread fields on unusual layouts
- Skill detection uses a fixed default list unless a custom list is provided
- Phone and portfolio URL extraction may return imperfect matches on some resumes

## Roadmap

- OCR support for scanned resumes
- DOCX and TXT file support
- Name, education, and experience extraction
- Section-based parsing
- Custom skill dictionary file path
- JSON schema output
- Batch parsing CLI

## Contributing

Contributions are welcome.

1. Fork [github.com/alixaprodev/resumeminer](https://github.com/alixaprodev/resumeminer)
2. Create a feature branch
3. Add tests for behavior changes
4. Run `pytest`
5. Open a pull request

Report issues on [GitHub Issues](https://github.com/alixaprodev/resumeminer/issues).

## License

MIT License. See [LICENSE](LICENSE).

## Author

**H. Ali**

- GitHub: [github.com/alixaprodev](https://github.com/alixaprodev)
- Email: [haxratali0@gmail.com](mailto:haxratali0@gmail.com)
