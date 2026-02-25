# Development Guide

This guide describes the day-to-day development workflow for automation engineers working on Dexter.

---

## Branching Strategy

| Branch | Purpose |
|--------|---------|
| `main` | Stable, always passing CI |
| `feature/<short-description>` | New features or tests |
| `fix/<short-description>` | Bug fixes |
| `chore/<short-description>` | Maintenance (deps, docs, config) |

**Workflow:**

```bash
# 1. Pull latest main
git checkout main && git pull

# 2. Create a feature branch
git checkout -b feature/add-order-sorting-tests

# 3. Make changes, commit often
git add .
git commit -m "test(api): add sorting validation for /api/orders"

# 4. Push and open a PR
git push -u origin feature/add-order-sorting-tests
```

---

## Running Tests Locally

Always run tests before pushing. Make sure your virtual environment is activated.

```bash
# All tests
pytest

# Only API tests
pytest -m api

# Only UI tests
pytest -m ui

# A single test file
pytest tests/api/test_orders_api.py

# A specific test by name
pytest -k "test_create_order"

# With coverage report
pytest --cov=src --cov-report=term-missing
```

> **Tip:** Run `pytest -x` to stop on the first failure — useful during active development.

---

## Linting and Formatting

This project uses `black` for code formatting and follows PEP 8.

```bash
# Check formatting (dry-run)
black --check .

# Apply formatting
black .
```

Run formatting before every commit to keep diffs clean.

---

## API Test Strategy

API tests live in `tests/api/` and use the Flask test client (no live server needed).

**Pattern:**

```python
def test_create_order(client):
    payload = {"item": "Widget", "price": 9.99, "qty": 2}
    response = client.post("/api/orders", json=payload)
    assert response.status_code == 201
    data = response.get_json()
    assert data["item"] == "Widget"
```

**Guidelines:**

- Use the `client` fixture from `tests/conftest.py`.
- Test one behaviour per test function.
- Include positive, negative, and boundary cases.
- Assert both status code and response body.

---

## UI Test Strategy

UI tests live in `tests/ui/` and use Selenium with headless Chrome.

**Pattern:**

```python
def test_create_order_ui(browser, live_server):
    browser.get(live_server + "/")
    browser.find_element(By.ID, "item").send_keys("Widget")
    browser.find_element(By.ID, "submit-btn").click()
    assert "Widget" in browser.find_element(By.ID, "order-list").text
```

**Guidelines:**

- Always use **explicit waits** (`WebDriverWait` + `expected_conditions`). Never use `time.sleep`.
- Use `By.ID` or `By.CSS_SELECTOR` — avoid fragile XPath selectors.
- Keep UI tests focused; prefer API tests for data-layer validation.
- See [Best Practices](best_practices.md) for more Selenium guidelines.

---

## Adding New Tests

### Add an API Test

1. Open (or create) a file under `tests/api/`.
2. Import the `client` fixture.
3. Write a function named `test_<behaviour>`.
4. Mark it with `@pytest.mark.api` so it can be run selectively.

```python
import pytest

@pytest.mark.api
def test_delete_nonexistent_order(client):
    response = client.delete("/api/orders/does-not-exist")
    assert response.status_code == 404
```

### Add a UI Test

1. Open (or create) a file under `tests/ui/`.
2. Import the `browser` and `live_server` fixtures.
3. Mark it with `@pytest.mark.ui`.
4. Use explicit waits for any dynamic elements.

---

## Debugging Tips

| Issue | What to do |
|-------|-----------|
| Test fails with `ConnectionRefusedError` | The Flask app is not running; use the `client` fixture instead of a live server for API tests |
| Selenium `NoSuchElementException` | The element may not be loaded yet; add `WebDriverWait` |
| Selenium `SessionNotCreatedException` | ChromeDriver version mismatch; update to match your Chrome version |
| `ModuleNotFoundError` | Virtual environment may not be activated; run `source .venv/bin/activate` |
| `AssertionError` on status code | Print `response.data` to see the actual response body |

**Print debugging in tests:**

```python
def test_something(client):
    response = client.get("/api/orders")
    print(response.get_json())   # visible with pytest -s
    assert response.status_code == 200
```

Run `pytest -s` to see print output during test execution.

---

## Related Guides

- [Onboarding](onboarding.md) — initial setup
- [Best Practices](best_practices.md) — automation patterns
- [CI/CD Guide](ci_cd.md) — running tests in GitHub Actions
- [Contributing](../CONTRIBUTING.md) — PR and commit conventions
