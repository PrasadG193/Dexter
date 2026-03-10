# Interview Prep

30+ Q&As organised by topic, with code examples drawn directly from this project. Use these to self-assess before a Python SDET interview.

---

## Python Basics

**Q1. What is the difference between a list and a tuple? Give an automation use case for each.**

A list is mutable (items can be added, removed, or changed). A tuple is immutable.
- Use a **list** to collect test results: `results = []` → `results.append(response.status_code)`.
- Use a **tuple** as a fixed set of parametrize inputs: `@pytest.mark.parametrize("qty,price", [(1, 9.99), (0, 9.99)])`.

---

**Q2. What is a list comprehension? Write one that extracts all `customer` names from a list of order dicts.**

```python
orders = [{"customer": "Alice", "price": 9.99}, {"customer": "Bob", "price": 4.99}]
names = [o["customer"] for o in orders]          # ["Alice", "Bob"]
cheap = [o["customer"] for o in orders if o["price"] < 5]  # ["Bob"]
```

---

**Q3. What are type hints and why do you use them in test code?**

Type hints (e.g., `def validate(data: dict) -> list[str]`) document expected types without enforcing them at runtime. In test code they:
- Improve IDE auto-complete and catch mistakes early with `mypy`.
- Make intent clear to reviewers ("this fixture returns a list of order dicts, not a single dict").

See `src/utils.py` for examples.

---

**Q4. What is a decorator? Name two pytest decorators.**

A decorator is a function that wraps another function to add behaviour without modifying its source.

```python
import functools

def timed(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        import time
        start = time.perf_counter()
        result = fn(*args, **kwargs)
        print(f"{fn.__name__} took {time.perf_counter() - start:.3f}s")
        return result
    return wrapper
```

Two pytest decorators: `@pytest.mark.parametrize` and `@pytest.fixture`.

---

**Q5. What is a dataclass? How does it differ from a regular class?**

A dataclass (`@dataclass`) auto-generates `__init__`, `__repr__`, and `__eq__` from field declarations:

```python
from dataclasses import dataclass, field
import uuid

@dataclass
class Order:
    customer: str
    price: float
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
```

Compared to a plain class, dataclasses eliminate boilerplate `__init__` code and are easier to read.

---

**Q6. How do you read a JSON file and return a list of dicts?**

```python
import json

def load_orders(path: str) -> list[dict]:
    with open(path) as f:
        return json.load(f)
```

In this project, `data/sample_orders.json` is loaded this way in the `sample_orders` fixture.

---

## pytest

**Q7. What is a pytest fixture and what problem does it solve?**

A fixture is a function decorated with `@pytest.fixture` that provides setup and teardown for tests. It solves the problem of repeated setup code by letting pytest inject shared resources:

```python
@pytest.fixture()
def client():
    flask_app.config["TESTING"] = True
    with flask_app.test_client() as c:
        yield c
    clear_orders()   # teardown
```

---

**Q8. What are fixture scopes and when do you use each?**

| Scope | Setup frequency | Use case |
|-------|----------------|----------|
| `function` (default) | Once per test | DB cleanup, test client |
| `module` | Once per test file | Starting a server thread |
| `session` | Once per `pytest` run | Expensive read-only resources |

In this project, `live_server` is `scope="module"` because starting Flask in a thread is expensive.

---

**Q9. What is `conftest.py` and what goes in it?**

`conftest.py` is a special pytest file where shared fixtures, hooks, and plugins are defined. pytest auto-discovers it — no import needed. In this project it contains `client`, `auth_headers`, `order_payload`, `sample_orders`, and the screenshot hook.

---

**Q10. How does `@pytest.mark.parametrize` work?**

```python
@pytest.mark.parametrize("qty,price,expected", [
    (2, 9.99, 201),
    (0, 9.99, 400),   # zero quantity
    (2, -1.0, 400),   # negative price
])
def test_create_order(client, auth_headers, qty, price, expected):
    res = client.post("/api/orders",
                      json={"customer": "X", "item": "Y", "quantity": qty, "price": price},
                      headers=auth_headers)
    assert res.status_code == expected
```

Each tuple is one test case. pytest generates a separate test ID for each.

---

**Q11. What is `pytest.approx` and when do you use it?**

`pytest.approx` handles floating-point comparison with a tolerance:

```python
assert data["revenue"] == pytest.approx(20.00)   # passes even with 19.999999...
```

Use it whenever comparing `float` values calculated by summing or multiplying.

---

**Q12. How do you run only a specific subset of tests?**

```bash
pytest -m api          # tests marked @pytest.mark.api
pytest -m "api or auth"
pytest -k "test_create"      # tests with "test_create" in the name
pytest tests/api/test_orders_api.py::test_health   # single test
```

---

## API Testing

**Q13. What is the difference between 400, 401, 403, 404, and 422?**

| Code | Meaning |
|------|---------|
| 400 | Bad Request — invalid or malformed input |
| 401 | Unauthorized — missing authentication |
| 403 | Forbidden — authenticated but not permitted |
| 404 | Not Found — resource does not exist |
| 422 | Unprocessable Entity — syntax valid but semantics invalid |

In this project, POST without `X-API-Key` returns 401; with a wrong key returns 403.

---

**Q14. What is idempotency and which HTTP methods are idempotent?**

An idempotent operation produces the same result no matter how many times it is repeated.
- **Idempotent:** GET, PUT, DELETE.
- **Not idempotent:** POST (each call creates a new resource).

This matters in tests: a DELETE test that runs twice will get 200 then 404.

---

**Q15. How do you test a paginated API endpoint?**

Test these cases:
1. Page 1 — correct `orders` count and `total`.
2. Last page — may have fewer items than `limit`.
3. `pages` metadata is correct (`ceil(total / limit)`).
4. Empty store — `total=0`, `pages=0` or `1`.

```python
data = client.get("/api/orders?page=2&limit=3").get_json()
assert len(data["orders"]) == 2    # only 2 items on last page
assert data["total"] == 5
assert data["pages"] == 2
```

---

**Q16. How do you test filtering and sorting?**

Create a known dataset, apply the filter/sort, and assert the exact result:

```python
# Sort ascending
for price in (20.00, 5.00, 15.00):
    client.post("/api/orders", json={..., "price": price}, headers=auth_headers)
orders = client.get("/api/orders?sort=price").get_json()["orders"]
assert [o["price"] for o in orders] == [5.00, 15.00, 20.00]
```

---

**Q17. How do you handle authentication headers in API tests without hardcoding secrets?**

Reference them via environment variables and expose them through a fixture:

```python
import os

@pytest.fixture()
def auth_headers():
    return {"X-API-Key": os.environ.get("API_KEY", "secret")}
```

In CI, set `API_KEY` as a GitHub Actions secret. In local dev the default `"secret"` is used.

---

**Q18. What is the difference between unit, integration, and end-to-end tests?**

| Type | Scope | Example in this project |
|------|-------|------------------------|
| Unit | Single function | Testing `validate_order_payload` directly |
| Integration | Multiple components together | Flask test client calling routes that use the data store |
| E2E | Full stack including UI | Selenium tests against the live Flask server |

---

## Selenium and UI Testing

**Q19. What is the difference between implicit and explicit waits?**

- **Implicit wait:** `driver.implicitly_wait(10)` — applied globally to every `find_element` call. Can hide real timing issues and slow tests unpredictably.
- **Explicit wait:** `WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element(...))` — waits for a specific condition. Preferred because it is deterministic and gives a clear failure message.

**Never use `time.sleep` in Selenium tests.**

---

**Q20. What is the Page Object Model (POM)?**

POM separates UI locators and interactions from test logic into dedicated "page" classes. Benefits:
- When a locator changes, only the page object needs updating.
- Tests read like user stories, not XPath expressions.
- Methods can be reused across tests.

In this project: `tests/ui/pages/order_page.py` contains all `find_element` calls; test functions only call `page.create_order(...)`.

---

**Q21. What are the best locator strategies in Selenium, in order of preference?**

1. `By.ID` — unique, fast, stable.
2. `By.CSS_SELECTOR` — flexible, readable, fast.
3. `By.NAME` / `By.CLASS_NAME` — use when ID is unavailable.
4. `By.XPATH` — last resort; brittle, verbose, slow.

---

**Q22. What causes flaky UI tests and how do you reduce them?**

Common causes:
- Race conditions — JS not finished before assertion (`time.sleep` mask these; explicit waits fix them).
- Shared test state — orders created in one test affect another.
- Environment instability — network, browser version mismatch.

Fixes:
- `WebDriverWait` for every dynamic element.
- `clear_orders()` at the start of each test.
- Screenshot on failure to diagnose intermittent failures.
- Pin browser and driver versions in CI.

---

**Q23. How do you capture a screenshot when a Selenium test fails?**

Use the `pytest_runtest_makereport` hook in `conftest.py`:

```python
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    if rep.when == "call" and rep.failed:
        driver = item.funcargs.get("driver")
        if driver is not None:
            driver.save_screenshot(f"reports/screenshots/{item.nodeid}.png")
```

---

## CI/CD

**Q24. Walk me through the GitHub Actions CI pipeline in this project.**

1. **Trigger:** Push or PR to `main`.
2. **Set up Python 3.12.**
3. **Install dependencies** from `requirements.txt`.
4. **Lint:** `black --check .` — fails if code is not formatted.
5. **API tests:** `pytest -m api --cov=src --cov-report=xml` — fails if coverage < 80%.
6. **Auth tests:** `pytest -m auth -v`.
7. **Install Chrome/ChromeDriver.**
8. **UI tests:** `pytest -m ui -v`.
9. **Upload artifacts:** `reports/report.html`, `coverage.xml`.

---

**Q25. How do you run only the API tests in CI?**

```yaml
- name: Run API tests
  run: pytest -m api -v
```

The `-m api` flag selects only tests marked with `@pytest.mark.api`.

---

**Q26. What is `--cov-fail-under` and when do you use it?**

```bash
pytest --cov=src --cov-fail-under=80
```

This makes the test run exit with a non-zero code if coverage falls below 80%, causing the CI job to fail. Use it to enforce a coverage floor and prevent regressions.

---

**Q27. What is the purpose of uploading artifacts in GitHub Actions?**

Artifacts preserve files from a CI run (HTML reports, screenshots, coverage XML) so you can download and inspect them after the run — even if the job failed. Without artifact upload, these files are lost when the runner VM shuts down.

---

## Soft Skills

**Q28. How do you decide which tests to automate versus test manually?**

Automate:
- High-frequency regression paths (every release)
- Data-driven scenarios with many input combinations
- Anything that is tedious or error-prone for a human

Test manually:
- Exploratory / session-based testing for new features
- Usability and visual design
- One-off edge cases unlikely to recur

---

**Q29. How do you keep a test suite maintainable as the app grows?**

1. Use the Page Object Model — one place for locators.
2. Use fixture factories — one place for test data.
3. Run tests in CI on every push — catch regressions immediately.
4. Delete or update tests when the feature changes rather than disabling them.
5. Keep tests fast — slow tests get skipped.
6. Name tests descriptively — `test_filter_by_status_returns_only_matching_orders` not `test_filter_1`.

---

**Q30. Describe your test strategy for a new feature.**

Example: adding the stats endpoint `/api/orders/stats`.

1. **Unit:** Test `calculate_order_total` in `src/utils.py` directly.
2. **API (happy path):** Create 2 orders, call `/api/orders/stats`, assert `total`, `revenue`, `by_status`.
3. **API (edge cases):** Empty store → revenue = 0. All statuses represented.
4. **Integration:** Verify the stats panel in the browser updates after creating an order via the UI.
5. **Auth:** GET is public — verify it returns 200 without a key.

---

**Q31. What would you do if a test started failing intermittently in CI?**

1. Check the CI screenshot (if UI) or response body logged on failure.
2. Look for shared state — does this test depend on order of execution?
3. Check for timing issues — replace any `sleep` with an explicit wait.
4. Reproduce locally with `pytest -x -v --count=5` (repeat runs).
5. Add logging to narrow the failure window.
6. If truly environment-related (network, resource exhaustion), quarantine the test and open a tracking issue.

---

## Related Guides

- [Training Plan](training_plan.md) — 15-day study schedule
- [Best Practices](best_practices.md) — patterns and anti-patterns
- [Tasks](tasks.md) — hands-on exercises
