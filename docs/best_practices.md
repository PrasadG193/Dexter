# Python Automation Best Practices

This guide collects automation engineering best practices applied throughout Dexter. Use it as a reference when writing or reviewing test code.

---

## Project Structure

Keep tests and source code clearly separated:

```
tests/
├── api/          ← API test modules
├── ui/
│   └── pages/    ← Page Object classes
└── conftest.py   ← Shared fixtures and hooks
```

- Name test files `test_<feature>.py`.
- Name test functions `test_<behaviour>_<condition>` (e.g., `test_create_order_returns_201`).
- Group related tests in the same module; split by domain, not by file size.

---

## Parametrized Testing

Use `@pytest.mark.parametrize` to test multiple inputs without duplicating code:

```python
import pytest

@pytest.mark.parametrize("payload", [
    {"customer": "X", "item": "Y", "quantity": 0, "price": 5.0},  # zero qty
    {"customer": "X", "item": "Y", "quantity": 2, "price": -1.0}, # negative price
    {"customer": "X", "item": "Y", "quantity": "two", "price": 5.0},  # wrong type
])
def test_create_order_invalid_payload(client, auth_headers, payload):
    res = client.post("/api/orders", json=payload, headers=auth_headers)
    assert res.status_code == 400
```

**When to use parametrize:**
- Same test logic, different inputs (boundary values, invalid payloads, status transitions)
- Replacing copy-paste tests that differ only in data
- Data-driven cases loaded from a JSON file

**Anti-patterns to avoid:**
- Hiding unrelated assertions inside a parametrized test
- Using parametrize when each case requires different setup or teardown

---

## Test Data Management

### Fixture factories

Use a factory pattern when tests need slight variations of the same data:

```python
@pytest.fixture()
def order_payload():
    def _make(customer="Alice", item="Widget", quantity=2, price=9.99):
        return {"customer": customer, "item": item, "quantity": quantity, "price": price}
    return _make

def test_create_order(client, auth_headers, order_payload):
    res = client.post("/api/orders", json=order_payload(customer="Bob"), headers=auth_headers)
    assert res.status_code == 201
```

### JSON data files

Use JSON files (`data/`) for large or reusable datasets. Load them in fixtures so test functions stay clean:

```python
@pytest.fixture()
def sample_orders(client, auth_headers):
    with open("data/sample_orders.json") as f:
        payloads = json.load(f)
    created = [client.post("/api/orders", json=p, headers=auth_headers).get_json() for p in payloads]
    yield created
    clear_orders()
```

### Rules
- Never hardcode expected values derived from test data directly in assertions — compute them.
- Always clean up created data in fixture teardown (after `yield`).
- Keep data files free of application logic; keep fixtures free of raw JSON strings.

---

## Page Object Model (POM)

The POM pattern separates UI locators and page interactions from test logic.

### Structure

```
tests/ui/
├── pages/
│   └── order_page.py   ← All find_element calls live here
└── test_orders_ui.py   ← Tests only call page object methods
```

### Key rules

1. **One class per page or significant UI component.**
2. **No `find_element` calls in test functions** — all Selenium interactions go in the page object.
3. **Return `self` from action methods** to enable fluent chaining:
   ```python
   page.open(base_url).create_order("Alice", "Widget", "2", "9.99")
   ```
4. **Keep waits inside the page object**, not in the test.

### Anti-patterns

- Putting assertions inside page object methods (keep assertions in tests)
- Using XPath everywhere — prefer `By.ID` and `By.CSS_SELECTOR` first
- Creating a single "God page object" with methods from multiple pages

---

## Explicit Waits in Selenium

**Never use `time.sleep`**. Use `WebDriverWait` with expected conditions:

```python
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

wait = WebDriverWait(driver, timeout=10)
wait.until(EC.text_to_be_present_in_element((By.ID, "orders-body"), "Alice"))
wait.until(lambda d: len(d.find_elements(By.CSS_SELECTOR, "#orders-body tr")) >= 2)
```

Use a 10-second default timeout. Document why a longer timeout is needed if you increase it.

---

## Coverage Targets

Run coverage with:
```bash
pytest -m api --cov=src --cov-report=term-missing
```

**Guidelines:**
- Target ≥ 80% overall coverage on `src/`.
- Aim for 100% on auth middleware and error-handling branches — these are highest risk.
- Missing coverage on `if __name__ == "__main__"` blocks is acceptable.
- Coverage measures execution, not correctness — pair it with meaningful assertions.

---

## Logging

Use Python's built-in `logging` module instead of `print` in application code:

```python
import logging
logger = logging.getLogger(__name__)

def create_order(order_data):
    logger.info("Creating order: %s", order_data)
```

In tests, `print` is acceptable for quick debugging but should be removed before merging.

---

## Error Handling

- Validate inputs early and return descriptive error responses.
- Test both the happy path and error paths.
- Use specific exception types, not bare `except Exception`.

```python
# Good
try:
    result = process_order(data)
except ValueError as exc:
    logger.error("Invalid order data: %s", exc)
    return {"error": str(exc)}, 400

# Avoid
try:
    result = process_order(data)
except:
    return {"error": "Something went wrong"}, 500
```

---

## Naming Conventions

| Item | Convention | Example |
|------|-----------|---------|
| Test file | `test_<feature>.py` | `test_orders_api.py` |
| Test function | `test_<behaviour>_<condition>` | `test_delete_order_returns_404` |
| Fixture | descriptive noun | `client`, `auth_headers`, `order_payload` |
| Page object | `<Page>Page` | `OrderPage` |
| Variable | `snake_case` | `order_id`, `response_body` |
| Constant | `UPPER_SNAKE_CASE` | `API_KEY`, `WAIT_TIMEOUT` |

---

## Code Review Checklist

Before submitting a PR, verify each item:

- [ ] Tests cover the happy path and at least one error/edge case
- [ ] No `time.sleep` in Selenium tests — `WebDriverWait` only
- [ ] No hardcoded credentials, URLs, or IDs (use fixtures or constants)
- [ ] `black .` applied — no formatting warnings
- [ ] All new test files are marked with the correct `@pytest.mark.*`
- [ ] Mutating API tests include `auth_headers` fixture
- [ ] Page object methods contain all `find_element` calls; none in test functions
- [ ] `pytest --cov=src` still shows ≥ 80% after your changes
- [ ] CI passes (GitHub Actions green)
- [ ] Commit messages follow Conventional Commits convention

---

## Additional Tips

- **Isolate tests:** Each test sets up its own data and does not rely on state from another test.
- **Use fixtures for setup/teardown:** Prefer `pytest` fixtures over `setUp`/`tearDown` classes.
- **Avoid test interdependence:** Tests must pass in any order.
- **Keep tests fast:** Avoid unnecessary network calls in unit/API tests.
- **Review flaky tests promptly:** A flaky test erodes trust in the entire suite.

---

## Related Guides

- [Development Guide](development_guide.md) — branching and test workflow
- [Onboarding](onboarding.md) — environment setup
- [Interview Prep](interview_prep.md) — common SDET interview questions
- [Contributing](../CONTRIBUTING.md) — PR conventions
