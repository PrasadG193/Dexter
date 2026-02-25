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

## Project Structure
```
Dexter/
├── .github/workflows/ci.yml
├── docs/
│   ├── ci_cd.md
│   ├── learning_path.md
│   └── tasks.md
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
└── README.md
```
