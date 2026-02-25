# Dexter — Practice Site

Welcome to the **Dexter** documentation hub. Dexter is a Python SDET automation learning module built around the **Order Board** app. Use this site to get started, explore tasks, and follow a structured training plan.

---

## Documentation

| Guide | Description |
|-------|-------------|
| [Onboarding](onboarding.md) | Environment setup, running the app, repo overview |
| [Learning Path](learning_path.md) | Phase-by-phase progression from Python basics to CI/CD |
| [Hands-on Tasks](tasks.md) | Incremental coding tasks to build real skills |
| [Training Plan](training_plan.md) | Structured 2-week daily plan with interview prep |
| [Development Guide](development_guide.md) | Branching, testing, linting, and debugging workflow |
| [Best Practices](best_practices.md) | Python automation patterns and code review checklist |
| [CI/CD Guide](ci_cd.md) | GitHub Actions workflow and troubleshooting |
| [Contributing](../CONTRIBUTING.md) | How to contribute, commit conventions, PR checklist |

---

## Run the App Locally

```bash
git clone https://github.com/prasadg-veeam/Dexter.git
cd Dexter
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python -m src.app
```

Open **http://localhost:5000** in your browser to see the Order Board UI.

Run tests:

```bash
pytest          # all tests
pytest -m api   # API tests only
pytest -m ui    # UI tests only
```

---

## Quick Links

- [GitHub Repository](https://github.com/prasadg-veeam/Dexter)
- [Open an Issue](https://github.com/prasadg-veeam/Dexter/issues)
- [Contributing Guide](../CONTRIBUTING.md)
