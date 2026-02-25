# CI/CD Guide

This project uses GitHub Actions to run automated tests on every push and pull request.

## Workflow Summary
- Install dependencies
- Run API tests
- Run UI tests in headless Chrome

## Workflow File
See: `.github/workflows/ci.yml`

## How to Trigger
1. Push a commit to `main` or open a Pull Request.
2. Open the **Actions** tab in GitHub and watch the workflow run.
3. Each job shows real-time logs — click a step to expand it.

## Running Specific Test Groups in CI

To run only API or UI tests, use pytest markers:

```yaml
- run: pytest -m api   # API tests only
- run: pytest -m ui    # UI tests only
```

Markers are defined in `pytest.ini`:

```ini
[pytest]
markers =
    api: REST API tests
    ui: Selenium UI tests
```

## Common Troubleshooting
- **Selenium errors**: Verify Chrome and chromedriver are installed correctly in the runner.
- **Flaky UI tests**: Use explicit waits in Selenium. See [Best Practices](best_practices.md).
- **Dependency issues**: Pin versions in `requirements.txt` if needed.
- **Formatting failures**: Run `black .` locally before pushing.

## Related Guides
- [Development Guide](development_guide.md) — local test and lint workflow
- [Best Practices](best_practices.md) — avoiding flaky tests
- [Contributing](../CONTRIBUTING.md) — PR checklist