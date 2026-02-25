# CI/CD Guide

This project uses GitHub Actions to run automated tests on every push and pull request.

## Workflow Summary
- Install dependencies
- Run API tests
- Run UI tests in headless Chrome

## Workflow File
See: `.github/workflows/ci.yml`

## How to Trigger
1. Push a commit to `main`.
2. Open the Actions tab and watch the workflow run.

## Common Troubleshooting
- **Selenium errors**: Verify Chrome and chromedriver are installed correctly in the runner.
- **Flaky UI tests**: Use explicit waits in Selenium.
- **Dependency issues**: Pin versions in `requirements.txt` if needed.