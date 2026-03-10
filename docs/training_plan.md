# Training Plan

A structured 3-week (15 business-day) plan for learning Python SDET skills using the Dexter project. Each day includes a topic summary, morning study activity, afternoon hands-on task, and interview angle.

---

## Overview

| Week | Focus | Days |
|------|-------|------|
| Week 1 | Python Foundations | 1–5 |
| Week 2 | API Test Automation | 6–10 |
| Week 3 | UI Automation + CI/CD | 11–15 |

---

## Week 1 — Python Foundations

### Day 1: Data Types and Collections

**Topic:** Python built-ins — `str`, `int`, `float`, `bool`, `list`, `dict`, `set`, `tuple`. List comprehensions and dict comprehensions.

**Morning:** Read the Python docs overview of [built-in types](https://docs.python.org/3/library/stdtypes.html). Then open `data/sample_orders.json` and read it with `json.load`.

**Afternoon task:**
- Create `scratch/day1_basics.py`.
- Load `data/sample_orders.json` and store it in a list.
- Use a list comprehension to filter orders where `quantity > 1`.
- Print the customer name and total cost (`price × quantity`) for each filtered order.

**Done when:** Script runs without errors and prints the correct filtered results.

**Task:** [→ Task 1: Python Basics](tasks.md#task-1-python-basics-day-1)

**Interview angle:** _"What is the difference between a list and a tuple? Give an automation use case for each."_ (Lists are mutable — good for collecting test results. Tuples are immutable — good for fixed test parameters.)

---

### Day 2: Functions, Type Hints, and Modules

**Topic:** Defining functions, default arguments, `*args`/`**kwargs`, type annotations, importing modules.

**Morning:** Read `src/utils.py`. Understand `validate_order_payload`, `format_price`, and `calculate_order_total`.

**Afternoon task:**
- Add a new function `summarise_orders(orders: list[dict]) -> str` to `src/utils.py` that returns a human-readable summary string.
- Write a standalone script `scratch/day2_utils.py` that loads `data/sample_orders.json`, calls all three utility functions, and prints the results.

**Done when:** `python scratch/day2_utils.py` prints a formatted summary with no errors.

**Task:** [→ Task 2: Functions and Type Hints](tasks.md#task-2-functions-and-type-hints-day-2)

**Interview angle:** _"What are type hints in Python and why do you use them in test code?"_ (Hints catch mistakes early, improve IDE auto-complete, and make intent clear to reviewers.)

---

### Day 3: Error Handling, Decorators, and Context Managers

**Topic:** `try/except/finally`, custom exceptions, `@` decorator syntax, `with` statement and context managers.

**Morning:** Read `src/utils.py:validate_order_payload`. Note how validation errors are collected rather than raised immediately.

**Afternoon task:**
- Add input validation to `validate_order_payload` that raises a `ValueError` if `data` is not a dict.
- Write `scratch/day3_errors.py` that calls `validate_order_payload` with three bad inputs and catches each error, printing a descriptive message.
- Add a simple timing decorator `@timed` (using `functools.wraps`) to a function in the scratch file.

**Done when:** All three error cases are handled gracefully and the timing output is printed.

**Task:** [→ Task 3: Error Handling](tasks.md#task-3-error-handling-day-3)

**Interview angle:** _"Describe what a decorator is and name two pytest decorators."_ (`@pytest.mark.parametrize` and `@pytest.fixture` are pytest decorators; a decorator is a function that wraps another function to add behaviour.)

---

### Day 4: OOP and Dataclasses

**Topic:** Classes, `__init__`, instance methods, inheritance, Python `@dataclass`.

**Morning:** Read `src/models.py`. Understand the `Order` dataclass — its fields, defaults, and `STATUS_TRANSITIONS`.

**Afternoon task:**
- Add an instance method `total_cost(self) -> float` to the `Order` dataclass that returns `price * quantity`.
- Write `scratch/day4_oop.py` that imports `Order` from `src.models`, creates two orders, and prints their `total_cost()`.
- Verify that `STATUS_TRANSITIONS["pending"]` contains `"fulfilled"` and `"cancelled"`.

**Done when:** `python scratch/day4_oop.py` prints correct totals and assertions pass.

**Task:** [→ Task 4: OOP and Dataclasses](tasks.md#task-4-oop-and-dataclasses-day-4)

**Interview angle:** _"What is a dataclass and how does it differ from a regular class?"_ (A dataclass auto-generates `__init__`, `__repr__`, and `__eq__` from field declarations, reducing boilerplate.)

---

### Day 5: Flask Basics and REST Concepts

**Topic:** HTTP methods and status codes, Flask routing, request/response cycle, JSON serialisation.

**Morning:** Start the app with `python -m src.app`. Use `curl` or Postman to call every endpoint:
- `GET /api/health`
- `GET /api/orders`
- `POST /api/orders` (with and without the `X-API-Key: secret` header)
- `GET /api/orders/stats`
- `GET /api/orders?status=pending`

**Afternoon task:**
- Read `src/app.py` end-to-end and add an inline comment above each route explaining what it does.
- Document the auth flow: which HTTP status code is returned when the key is missing (401) vs. wrong (403)?
- Answer in a `scratch/day5_notes.md` file: _What is the difference between 400, 401, 403, 404, and 422?_

**Done when:** All curl calls succeed as expected and notes file is complete.

**Task:** [→ Task 5: App Exploration with curl](tasks.md#task-5-app-exploration-with-curl-day-5)

**Interview angle:** _"What is the difference between a 400 and a 422?"_ (400 is generic bad request; 422 Unprocessable Entity is used when the syntax is valid but semantics fail — e.g., JSON is valid but a field value is out of range.)

---

## Week 2 — API Test Automation

### Day 6: pytest Fundamentals and Fixtures

**Topic:** Test discovery, `assert` statements, `pytest.raises`, fixture scope (`function`, `module`, `session`), `conftest.py`.

**Morning:** Read `tests/conftest.py` and `tests/api/test_orders_api.py`. Note how `client`, `auth_headers`, and `order_payload` fixtures work.

**Afternoon task:**
- Write 5 new API tests in `tests/api/test_orders_api.py` covering edge cases you find by reading `src/app.py`.
- At least two tests must use the `order_payload` factory fixture.
- Run `pytest -m api -v` and confirm all pass.

**Done when:** `pytest -m api -v` shows all new tests green.

**Task:** [→ Task 6: pytest Fundamentals](tasks.md#task-6-pytest-fundamentals-day-6)

**Interview angle:** _"What is the difference between `function` and `module` scope in a pytest fixture?"_ (Function: fixture is set up and torn down for each test. Module: shared once across all tests in the file — good for expensive setup like starting a server.)

---

### Day 7: Parametrized Tests and Boundary Testing

**Topic:** `@pytest.mark.parametrize`, boundary value analysis, equivalence partitioning.

**Morning:** Read the existing `test_create_order_invalid_payload` parametrized test. Understand how each parameter tuple maps to a test case.

**Afternoon task:**
- Add a new parametrized test `test_update_order_statuses` that tests every valid status transition (`pending→fulfilled`, `pending→cancelled`) and at least two invalid ones (`fulfilled→pending`, `cancelled→pending`).
- Add a parametrized test for `GET /api/orders?sort=X` with valid and invalid sort values.

**Done when:** All parametrized cases pass; invalid transitions return 400.

**Task:** [→ Task 7: Parametrized Tests](tasks.md#task-7-parametrized-tests-day-7)

**Interview angle:** _"What is boundary value analysis and when do you apply it?"_ (Test values just inside and outside valid ranges — e.g., quantity=0, 1, and INT_MAX — to catch off-by-one errors.)

---

### Day 8: Test Data Management and JSON Fixtures

**Topic:** Fixture factories, loading JSON test data, the `sample_orders` fixture, separating test data from test logic.

**Morning:** Read `data/sample_orders.json` and the `sample_orders` fixture in `tests/conftest.py`. Understand how it creates orders and cleans up.

**Afternoon task:**
- Write a test `test_stats_with_sample_data` in `tests/api/test_filters_api.py` that uses the `sample_orders` fixture and asserts the `/api/orders/stats` revenue matches the expected sum.
- Add a second JSON file `data/invalid_orders.json` with 3 invalid payloads and write a parametrized test that loads it with `json.load` and asserts each returns 400.

**Done when:** Both tests pass; data files are separate from test logic.

**Task:** [→ Task 8: JSON Test Data Fixtures](tasks.md#task-8-json-test-data-fixtures-day-8)

**Interview angle:** _"How do you manage test data in a large test suite?"_ (Use fixtures for programmatic setup, JSON/CSV files for data-driven cases, and always clean up with teardown or autouse fixtures.)

---

### Day 9: Authentication Testing

**Topic:** API key auth, HTTP 401 vs. 403, testing security boundaries.

**Morning:** Read `tests/api/test_auth_api.py`. Understand why 401 means "unauthenticated" and 403 means "authenticated but not authorised".

**Afternoon task:**
- Verify all tests in `test_auth_api.py` pass: `pytest -m auth -v`.
- Add a test that checks the error message body for missing vs. wrong key (they should differ).
- Write `scratch/day9_notes.md` answering: _How would you test an OAuth2 bearer-token API instead of an API key?_

**Done when:** `pytest -m auth -v` is all green; notes file answers the question.

**Task:** [→ Task 9: Auth Tests](tasks.md#task-9-auth-tests-day-9)

**Interview angle:** _"How do you handle authentication headers in API tests without hardcoding secrets?"_ (Use environment variables or a secrets manager; reference them via `os.environ.get()` in fixtures.)

---

### Day 10: Filtering, Pagination, and Stats Tests

**Topic:** Query parameters, paginated responses, aggregate endpoints, using `pytest.approx` for floats.

**Morning:** Read `tests/api/test_filters_api.py` end-to-end.

**Afternoon task:**
- Add a test that creates 7 orders and verifies `pages=3` when `limit=3`.
- Add a test that filters by customer _and_ status simultaneously (combine query params: `?customer=Alice&status=pending`).
- Run `pytest -m api -v` — all tests should pass.

**Done when:** All new tests pass; `pytest.approx` is used where floating-point equality is tested.

**Task:** [→ Task 10: Filtering and Pagination Tests](tasks.md#task-10-filtering-and-pagination-tests-day-10)

**Interview angle:** _"How do you test a paginated API endpoint?"_ (Test page 1 and 2, boundary (empty last page), and that `total` and `pages` metadata are correct.)

---

## Week 3 — UI Automation + CI/CD

### Day 11: Selenium Basics and Explicit Waits

**Topic:** WebDriver setup, locator strategies (`By.ID`, `By.CSS_SELECTOR`, `By.XPATH`), `WebDriverWait` with `ExpectedConditions`.

**Morning:** Read `tests/ui/test_orders_ui.py`. Note how `live_server` starts Flask in a thread and how `driver` yields and quits Chrome.

**Afternoon task:**
- Run `pytest -m ui -v` and confirm the existing 4 tests pass.
- Write a new UI test `test_order_count_increases` that creates two orders via the UI and asserts the orders table has at least two rows.
- **Never use `time.sleep`** — use `WebDriverWait` only.

**Done when:** All 5 UI tests pass with no `sleep` calls.

**Task:** [→ Task 11: Selenium Basics](tasks.md#task-11-selenium-basics-day-11)

**Interview angle:** _"What is the difference between implicit and explicit waits in Selenium?"_ (Implicit: global timeout applied to every `find_element` call — can hide real timing issues. Explicit: per-condition wait that fails fast with a clear reason — preferred.)

---

### Day 12: Page Object Model

**Topic:** POM pattern, single responsibility, method chaining, why POM reduces test maintenance.

**Morning:** Read `tests/ui/pages/order_page.py`. Understand every method and the rationale for the fluent interface (returning `self`).

**Afternoon task:**
- Add a `filter_by_status` test to `tests/ui/test_orders_ui.py` that uses `OrderPage.filter_by_status("fulfilled")` and asserts only fulfilled orders are shown.
- Add a `get_error_message(self) -> str` method to `OrderPage` that reads the `#error-msg` element.
- Write a test that submits an empty form and asserts the error message is not empty.

**Done when:** All new UI tests pass; `OrderPage` is the only file that contains Selenium `find_element` calls.

**Task:** [→ Task 12: Page Object Model](tasks.md#task-12-page-object-model-day-12)

**Interview angle:** _"What is the Page Object Model and why do you use it?"_ (POM separates locators and page actions from test logic. When the UI changes, only the page object needs updating — not every test.)

---

### Day 13: Screenshot on Failure and Advanced UI Testing

**Topic:** `pytest_runtest_makereport` hook, screenshot capture, debugging failed UI tests.

**Morning:** Read the `pytest_runtest_makereport` hook in `tests/conftest.py`. Understand how `item.funcargs.get("driver")` retrieves the fixture value.

**Afternoon task:**
- Intentionally break one UI test (e.g., wrong locator). Run `pytest -m ui -v` and verify a screenshot is saved to `reports/screenshots/`.
- Fix the test. Run again and verify no screenshot is saved for passing tests.
- Write `scratch/day13_notes.md` answering: _What information would you include in a failure screenshot filename?_

**Done when:** Screenshot is saved on failure; none saved on pass.

**Task:** [→ Task 13: Screenshot on Failure](tasks.md#task-13-screenshot-on-failure-day-13)

**Interview angle:** _"How do you debug a flaky Selenium test?"_ (Add screenshot on failure, increase timeouts, log browser console errors, check for race conditions in async JS, and isolate state between tests.)

---

### Day 14: Coverage, HTML Reports, and Code Quality

**Topic:** `pytest-cov`, branch coverage, `pytest-html`, `black` formatter, coverage thresholds.

**Morning:** Run the following commands and read the output:
```bash
pytest -m api --cov=src --cov-report=term-missing
black --check .
open reports/report.html
```

**Afternoon task:**
- Identify two uncovered branches in `src/app.py` or `src/data_store.py` and write tests that cover them.
- Run `pytest --cov=src --cov-report=term-missing` and confirm coverage is ≥ 80%.
- Fix any `black` violations.

**Done when:** Coverage ≥ 80%; `black --check .` exits 0; `reports/report.html` shows all tests.

**Task:** [→ Task 14: Coverage and HTML Reports](tasks.md#task-14-coverage-and-html-reports-day-14)

**Interview angle:** _"What does 80% code coverage mean? Is it enough?"_ (80% is a common threshold. It is a floor, not a goal — critical paths like auth and error handling should be 100%; utility code can be lower. Coverage does not guarantee correctness.)

---

### Day 15: CI/CD Deep Dive and Interview Prep

**Topic:** GitHub Actions triggers, job steps, artifact upload, matrix builds, mock interview.

**Morning:** Read `.github/workflows/ci.yml` end-to-end. Identify: what triggers the workflow, which jobs run, what is uploaded as an artifact.

**Afternoon task:**
- Push a branch with a deliberate test failure. Observe the CI failure in the Actions tab. Fix it and re-push.
- Answer each question in [Interview Prep](interview_prep.md) out loud (or in writing).
- Write 2–3 sentences for a resume bullet point describing this project.

**Done when:** CI is green on your branch; interview prep questions answered.

**Task:** [→ Task 15: CI/CD and Interview Prep](tasks.md#task-15-cicd-and-interview-prep-day-15)

**Interview angle:** _"Walk me through the CI pipeline for this project."_ (Push triggers checkout → install deps → `black --check` → API tests with coverage → Chrome install → UI tests → upload reports.)

---

## Expected Outcomes

By the end of 15 days you will be able to:

1. Write Python with proper type hints, error handling, and OOP design.
2. Design and automate REST API tests with `pytest`, including parametrized, auth, and pagination tests.
3. Write UI tests with Selenium using the Page Object Model and explicit waits.
4. Measure and improve test coverage with `pytest-cov`.
5. Generate HTML reports and capture screenshots on failure.
6. Operate and debug a GitHub Actions CI pipeline.
7. Answer common Python SDET interview questions with confidence.

---

## Related Guides

- [Onboarding](onboarding.md) — environment setup
- [Learning Path](learning_path.md) — phase-by-phase progression
- [Hands-on Tasks](tasks.md) — one task per day
- [Best Practices](best_practices.md) — automation patterns
- [Interview Prep](interview_prep.md) — 30+ Q&As
- [Development Guide](development_guide.md) — branching and workflow
