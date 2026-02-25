# Onboarding Guide

Welcome to **Dexter** — a Python SDET automation learning module built around the **Order Board** app. This guide gets you set up and productive as quickly as possible.

---

## Project Overview

Dexter is a self-contained practice project that simulates a real-world automation engineering workflow. You will:

- Run a small Flask web application (Order Board)
- Write and extend REST API tests with `pytest`
- Write and extend UI tests with Selenium (headless Chrome)
- Work with GitHub Actions CI/CD
- Follow automation best practices used in professional environments

---

## Prerequisites

| Requirement | Version |
|-------------|---------|
| Python | 3.9 or later |
| pip | Latest (bundled with Python) |
| Git | Any recent version |
| Google Chrome | Latest stable |
| ChromeDriver | Must match your Chrome version |

> **Windows users:** Use Git Bash or WSL2 for the best experience with the commands below.

---

## Environment Setup

### 1. Clone the Repository

```bash
git clone https://github.com/prasadg-veeam/Dexter.git
cd Dexter
```

### 2. Create and Activate a Virtual Environment

```bash
python -m venv .venv
# macOS / Linux
source .venv/bin/activate
# Windows (Git Bash)
source .venv/Scripts/activate
# Windows (cmd)
.venv\Scripts\activate.bat
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Running the Application

Start the Flask development server:

```bash
python -m src.app
```

The app is now available at **http://localhost:5000**.

- **UI:** Open `http://localhost:5000` in your browser to see the Order Board.
- **API:** Use curl or Postman to call the REST endpoints.

### Key API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/health` | Health check |
| GET | `/api/orders` | List all orders |
| POST | `/api/orders` | Create a new order |
| PUT | `/api/orders/<id>` | Update an order |
| DELETE | `/api/orders/<id>` | Delete an order |

**Example:**

```bash
# Health check
curl http://localhost:5000/api/health

# Create an order
curl -X POST http://localhost:5000/api/orders \
  -H "Content-Type: application/json" \
  -d '{"item": "Widget", "price": 9.99, "qty": 2}'

# List all orders
curl http://localhost:5000/api/orders
```

---

## Running Tests

Make sure the virtual environment is activated, then:

```bash
# Run all tests
pytest

# Run only API tests
pytest -m api

# Run only UI tests
pytest -m ui

# Run with verbose output
pytest -v
```

> UI tests require Chrome and ChromeDriver. See [CI/CD Guide](ci_cd.md) for headless setup details.

---

## Navigating the Repository

```
Dexter/
├── .github/workflows/ci.yml   ← GitHub Actions workflow
├── docs/                       ← All documentation
│   ├── index.md                ← GitHub Pages landing page
│   ├── onboarding.md           ← This file
│   ├── development_guide.md    ← Dev workflow for automation engineers
│   ├── best_practices.md       ← Python automation best practices
│   ├── training_plan.md        ← Structured trainee plan
│   ├── learning_path.md        ← Phase-by-phase learning path
│   ├── tasks.md                ← Hands-on tasks
│   └── ci_cd.md                ← CI/CD guide
├── src/
│   ├── app.py                  ← Flask app entry point and routes
│   ├── data_store.py           ← In-memory data layer
│   ├── static/app.js           ← Front-end JavaScript
│   └── templates/index.html   ← HTML template
├── tests/
│   ├── api/                    ← API test files
│   ├── ui/                     ← UI (Selenium) test files
│   └── conftest.py             ← pytest fixtures
├── pytest.ini                  ← pytest configuration
├── requirements.txt            ← Python dependencies
├── CONTRIBUTING.md             ← Contribution guidelines
└── README.md                  ← Project overview
```

---

## Next Steps

1. Read [Learning Path](learning_path.md) for a phase-by-phase progression plan.
2. Read [Development Guide](development_guide.md) for branching and test workflow.
3. Work through [Hands-on Tasks](tasks.md) to build skills incrementally.
4. Follow the [Training Plan](training_plan.md) for a structured daily schedule.
