# Sample resume PDFs

Real, publicly available resume PDFs for manual and integration testing.

| File | Source | Notes |
|------|--------|-------|
| `awesome_cv_resume.pdf` | [Awesome-CV example](https://github.com/posquit0/Awesome-CV/blob/master/examples/resume.pdf) | LaTeX resume (Byungjin Park) |
| `awesome_cv_cv.pdf` | [Awesome-CV CV example](https://github.com/posquit0/Awesome-CV/blob/master/examples/cv.pdf) | Longer CV variant |
| `software_engineer_resume.pdf` | [Software Engineer Resume Template](https://github.com/dev-amr-elsherif/software-engineer-resume-template) | One-page software engineer resume |

These files are **not** committed for redistribution beyond testing in this repo. They remain the property of their respective authors and are used here only as realistic parsing samples.

## Try them locally

```bash
resumeminer parse tests/fixtures/software_engineer_resume.pdf --json
```

```python
from resumeminer import parse_resume

result = parse_resume("tests/fixtures/awesome_cv_resume.pdf")
print(result["email"], result["skills"])
```

## Re-download

```bash
curl -L -o tests/fixtures/awesome_cv_resume.pdf \
  https://raw.githubusercontent.com/posquit0/Awesome-CV/master/examples/resume.pdf

curl -L -o tests/fixtures/awesome_cv_cv.pdf \
  https://raw.githubusercontent.com/posquit0/Awesome-CV/master/examples/cv.pdf

curl -L -o tests/fixtures/software_engineer_resume.pdf \
  https://raw.githubusercontent.com/dev-amr-elsherif/software-engineer-resume-template/main/resume.pdf
```
