# Contributing to Dexter

Thank you for contributing to Dexter! This guide explains everything you need to know to make a clean, mergeable contribution.

---

## Code of Conduct

Be respectful and constructive in all interactions. Harassment, personal attacks, or discriminatory language will not be tolerated.

---

## Setup

1. **Fork** the repository and clone your fork:

   ```bash
   git clone https://github.com/<your-username>/Dexter.git
   cd Dexter
   ```

2. **Create a virtual environment** and install dependencies:

   ```bash
   python -m venv .venv
   source .venv/bin/activate   # Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. See [Onboarding Guide](docs/onboarding.md) for full setup details.

---

## Running Tests

```bash
# All tests
pytest

# API tests only
pytest -m api

# UI tests only
pytest -m ui
```

All tests must pass before opening a PR.

---

## Code Formatting

This project uses [black](https://black.readthedocs.io/) for consistent formatting.

```bash
# Check (no changes applied)
black --check .

# Apply formatting
black .
```

Run `black .` before every commit.

---

## Commit Message Conventions

Use the [Conventional Commits](https://www.conventionalcommits.org/) format:

```
<type>(<scope>): <short description>
```

| Type | When to use |
|------|-------------|
| `feat` | New feature or test |
| `fix` | Bug fix |
| `test` | Adding or updating tests only |
| `docs` | Documentation changes |
| `chore` | Maintenance (deps, config, CI) |
| `refactor` | Code restructuring without behaviour change |

**Examples:**

```
feat(api): add DELETE /api/orders endpoint
test(ui): add validation message test for empty form
fix(api): return 404 when order id not found
docs: add onboarding guide
chore: pin black to 24.x in requirements.txt
```

---

## Branching

Create branches from `main`:

```
feature/<short-description>
fix/<short-description>
chore/<short-description>
docs/<short-description>
```

---

## Pull Request Checklist

Before marking your PR as ready for review, confirm:

- [ ] Branch is up to date with `main`
- [ ] All tests pass locally (`pytest`)
- [ ] `black .` applied — no formatting warnings
- [ ] New tests are marked `@pytest.mark.api` or `@pytest.mark.ui`
- [ ] Commit messages follow the conventions above
- [ ] PR title follows the commit convention (e.g., `feat(api): add sorting endpoint`)
- [ ] PR description explains **what** changed and **why**
- [ ] CI passes (GitHub Actions green)
- [ ] Related documentation updated if needed

---

## Getting Help

If you have questions, open an issue with the `question` label or start a discussion on GitHub.
