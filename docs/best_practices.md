# Python Automation Best Practices

This guide collects automation engineering best practices applied throughout Dexter. Use it as a reference when writing or reviewing test code.

---

## Project Structure

Keep tests and source code clearly separated:

```
tests/
├── api/          ← API test modules
├── ui/           ← UI (Selenium) test modules
└── conftest.py   ← Shared fixtures and configuration
```

- Name test files `test_<feature>.py`.
- Name test functions `test_<behaviour>_<condition>` (e.g., `test_create_order_returns_201`).
- Group related tests in the same module; split by domain, not by file size.

---

## Data-Driven Tests

Use `pytest.mark.parametrize` to test multiple inputs without duplicating code:

```python
import pytest

@pytest.mark.parametrize("item,price,qty,expected_status", [
    ("Widget", 9.99, 2, 201),
    ("",       9.99, 2, 400),   # missing item
    ("Widget", -1,   2, 400),   # negative price
])
def test_create_order_validation(client, item, price, qty, expected_status):
    response = client.post("/api/orders", json={"item": item, "price": price, "qty": qty})
    assert response.status_code == expected_status
```

---

## Explicit Waits in Selenium

**Never use `time.sleep`**. Use `WebDriverWait` with expected conditions:

```python
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

wait = WebDriverWait(driver, timeout=10)

# Wait until an element is visible
element = wait.until(EC.visibility_of_element_located((By.ID, "order-list")))

# Wait until text appears
wait.until(EC.text_to_be_present_in_element((By.ID, "status"), "Success"))
```

Set a sensible default timeout (10 seconds) and document why a longer timeout is needed if you use one.

---

## Logging

Use Python's built-in `logging` module instead of `print` statements in application code:

```python
import logging

logger = logging.getLogger(__name__)

def create_order(order_data):
    logger.info("Creating order: %s", order_data)
    # ...
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
| Test function | `test_<behaviour>_<condition>` | `test_delete_order_returns_204` |
| Fixture | descriptive noun | `client`, `browser`, `sample_order` |
| Variable | `snake_case` | `order_id`, `response_body` |
| Constant | `UPPER_SNAKE_CASE` | `BASE_URL`, `DEFAULT_TIMEOUT` |

---

## Code Review Checklist

Before submitting a PR, verify each item:

- [ ] Tests cover the happy path and at least one error/edge case
- [ ] No `time.sleep` in Selenium tests
- [ ] No hardcoded credentials, URLs, or IDs (use fixtures or constants)
- [ ] `black .` applied — no formatting warnings
- [ ] All new functions and fixtures have a short docstring
- [ ] Commit messages follow the convention (see [CONTRIBUTING.md](../CONTRIBUTING.md))
- [ ] CI passes (GitHub Actions green)
- [ ] New test files are marked with `@pytest.mark.api` or `@pytest.mark.ui`

---

## Additional Tips

- **Isolate tests:** Each test should set up its own data and not rely on state left by another test.
- **Use fixtures for setup/teardown:** Prefer `pytest` fixtures over `setUp`/`tearDown` classes.
- **Avoid test interdependence:** Tests must pass in any order.
- **Keep tests fast:** Mock external dependencies; avoid unnecessary network calls.
- **Review flaky tests promptly:** A flaky test is worse than no test — it erodes trust in the suite.

---

## Related Guides

- [Development Guide](development_guide.md) — branching and test workflow
- [Onboarding](onboarding.md) — environment setup
- [Contributing](../CONTRIBUTING.md) — PR conventions
