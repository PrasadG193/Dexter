# Dexter

## Project Goal
Dexter is a Python SDET automation learning module built around a small project called **Order Board**. You learn Python fundamentals by building and automating a real, testable app that exposes REST APIs and a simple web UI.

## What You Will Practice
- Python basics (data structures, functions, error handling)
- REST API automation with `pytest` + Flask test client
- UI automation with Selenium (headless Chrome)
- Test organization, fixtures, and assertions
- GitHub Actions CI for real-world workflow

## Quickstart
1. Clone the repo:
   ```bash
   git clone https://github.com/prasadg-veeam/Dexter.git
   cd Dexter
   ```
2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```
3. Run the app:
   ```bash
   python -m src.app
   ```
4. Run tests:
   ```bash
   pytest
   ```

## Learning Path and Tasks
- **Learning path:** `docs/learning_path.md`
- **Hands-on tasks:** `docs/tasks.md`
- **CI/CD guide:** `docs/ci_cd.md`
- **Onboarding:** `docs/onboarding.md`
- **Development guide:** `docs/development_guide.md`
- **Best practices:** `docs/best_practices.md`
- **Training plan:** `docs/training_plan.md`

## Practice Site (GitHub Pages)

The documentation is hosted as a GitHub Pages site at:

**https://prasadg-veeam.github.io/Dexter/**

> **Note:** GitHub Pages must be enabled in the repository settings. Go to **Settings → Pages**, set the source to the `main` branch and the `/docs` folder, then save.

## Project Structure
```
Dexter/
├── .github/workflows/ci.yml
├── docs/
│   ├── index.md               ← GitHub Pages landing page
│   ├── onboarding.md
│   ├── development_guide.md
│   ├── best_practices.md
│   ├── training_plan.md
│   ├── learning_path.md
│   ├── tasks.md
│   └── ci_cd.md
├── src/
│   ├── app.py
│   ├── data_store.py
│   ├── static/
│   │   └── app.js
│   └── templates/
│       └── index.html
├── tests/
│   ├── api/
│   ├── ui/
│   └── conftest.py
├── pytest.ini
├── requirements.txt
├── CONTRIBUTING.md
└── README.md
```
