# Hands-on Tasks

One task per day of the [Training Plan](training_plan.md). Start with Task 1 and proceed sequentially — each task builds on the previous one.

> **New to the project?** See [Onboarding](onboarding.md) to set up your environment first.
> Review [Best Practices](best_practices.md) before submitting your work.

---

## Task 1: Python Basics (Day 1)

**Training Plan:** [→ Day 1: Data Types and Collections](training_plan.md#day-1-data-types-and-collections)

**Goal:** Parse JSON data and manipulate it with Python collections.

**Steps:**
1. Create `scratch/day1_basics.py`.
2. Open and load `data/sample_orders.json` using `json.load`.
3. Filter orders where `quantity > 1` using a list comprehension.
4. For each filtered order, print `f"{customer}: ${price * quantity:.2f}"`.

**Hints:** `with open(path) as f: data = json.load(f)` — list comprehension syntax is `[x for x in items if condition]`.

**Done when:** Running `python scratch/day1_basics.py` prints 3–4 lines with no errors.

---

## Task 2: Functions and Type Hints (Day 2)

**Training Plan:** [→ Day 2: Functions, Type Hints, and Modules](training_plan.md#day-2-functions-type-hints-and-modules)

**Goal:** Write and use helper functions from `src/utils.py`.

**Steps:**
1. Read all three functions in `src/utils.py`.
2. Add `summarise_orders(orders: list[dict]) -> str` that returns a multi-line summary.
3. Create `scratch/day2_utils.py` that loads the JSON and calls all four utility functions.
4. Print the results.

**Hints:** `calculate_order_total` expects a list of dicts with `"price"` and `"quantity"` keys.

**Done when:** `python scratch/day2_utils.py` prints a formatted summary with no errors; `black --check .` exits 0.

---

## Task 3: Error Handling (Day 3)

**Training Plan:** [→ Day 3: Error Handling, Decorators, and Context Managers](training_plan.md#day-3-error-handling-decorators-and-context-managers)

**Goal:** Handle exceptions gracefully and understand context managers.

**Steps:**
1. Add a guard to `validate_order_payload` in `src/utils.py` that raises `TypeError` if `data` is not a dict.
2. Create `scratch/day3_errors.py` with three calls to `validate_order_payload`: one with `None`, one with a list, one with a dict missing `item`.
3. Wrap each call in `try/except` and print a descriptive message.
4. Add a `@timed` decorator using `functools.wraps` to any function in the file.

**Hints:** `isinstance(data, dict)` — `functools.wraps` preserves the wrapped function's `__name__`.

**Done when:** All three error cases print clear messages; timing output is shown.

---

## Task 4: OOP and Dataclasses (Day 4)

**Training Plan:** [→ Day 4: OOP and Dataclasses](training_plan.md#day-4-oop-and-dataclasses)

**Goal:** Understand and extend the `Order` dataclass.

**Steps:**
1. Read `src/models.py`.
2. Add `total_cost(self) -> float` to the `Order` dataclass returning `price * quantity`.
3. Create `scratch/day4_oop.py` that imports `Order` and creates two orders with different prices and quantities.
4. Print each order's `total_cost()` and verify `STATUS_TRANSITIONS["pending"]` contains both target statuses.

**Hints:** Add instance methods to a dataclass the same way as a regular class — no special syntax needed.

**Done when:** `python scratch/day4_oop.py` prints correct totals; no `AttributeError`.

---

## Task 5: App Exploration with curl (Day 5)

**Training Plan:** [→ Day 5: Flask Basics and REST Concepts](training_plan.md#day-5-flask-basics-and-rest-concepts)

**Goal:** Understand every REST endpoint and the auth middleware.

**Steps:**
1. Start the app: `python -m src.app`.
2. Run each of these curl commands and record the response status and body:
   - `curl http://localhost:5000/api/health`
   - `curl http://localhost:5000/api/orders`
   - `curl -X POST http://localhost:5000/api/orders -H "Content-Type: application/json" -d '{"customer":"Test","item":"X","quantity":1,"price":5.0}'`
   - Same POST with `-H "X-API-Key: secret"` added.
   - `curl http://localhost:5000/api/orders/stats`
   - `curl "http://localhost:5000/api/orders?status=pending"`
3. Write findings in `scratch/day5_notes.md`.

**Done when:** Notes file documents status codes and response bodies for all 6 calls.

---

## Task 6: pytest Fundamentals (Day 6)

**Training Plan:** [→ Day 6: pytest Fundamentals and Fixtures](training_plan.md#day-6-pytest-fundamentals-and-fixtures)

**Goal:** Write 5 new API tests using fixtures.

**Steps:**
1. Read `tests/conftest.py` and `tests/api/test_orders_api.py`.
2. Add 5 new tests in `tests/api/test_orders_api.py` using the `order_payload` factory fixture.
3. Cover: listing multiple orders, updating item/quantity fields, updating price, and at least two edge cases you find by reading `src/app.py`.
4. Run `pytest -m api -v` — all must pass.

**Hints:** `order_payload(customer="Bob")` returns a dict you can pass directly to `client.post`.

**Done when:** `pytest -m api -v` shows all tests green with no warnings.

---

## Task 7: Parametrized Tests (Day 7)

**Training Plan:** [→ Day 7: Parametrized Tests and Boundary Testing](training_plan.md#day-7-parametrized-tests-and-boundary-testing)

**Goal:** Use `@pytest.mark.parametrize` to test multiple inputs efficiently.

**Steps:**
1. Add a parametrized test for all status transitions (valid and invalid) using a list of `(from_status, to_status, expected_code)` tuples.
2. Valid transitions: `("pending", "fulfilled", 200)`, `("pending", "cancelled", 200)`.
3. Invalid: `("fulfilled", "pending", 400)`, `("cancelled", "fulfilled", 400)`, `("cancelled", "pending", 400)`.
4. Run `pytest -m api -v`.

**Hints:** The test must create an order and PUT to set the initial status before testing the transition.

**Done when:** All 5 parametrized cases pass; `pytest -m api -v` is green.

---

## Task 8: JSON Test Data Fixtures (Day 8)

**Training Plan:** [→ Day 8: Test Data Management and JSON Fixtures](training_plan.md#day-8-test-data-management-and-json-fixtures)

**Goal:** Separate test data from test logic using JSON files and fixtures.

**Steps:**
1. Verify `data/sample_orders.json` has 5 entries.
2. Write `test_stats_with_sample_data` in `tests/api/test_filters_api.py` using the `sample_orders` fixture.
3. Assert `revenue` from `/api/orders/stats` equals `sum(o["price"] * o["quantity"] for o in sample_orders)` using `pytest.approx`.
4. Create `data/invalid_orders.json` with 3 invalid payloads (missing fields, wrong types, negative values).
5. Write a parametrized test that loads the file and asserts each returns 400.

**Done when:** Both tests pass; data files contain no hard-coded expected values in test code.

---

## Task 9: Auth Tests (Day 9)

**Training Plan:** [→ Day 9: Authentication Testing](training_plan.md#day-9-authentication-testing)

**Goal:** Test API key authentication thoroughly.

**Steps:**
1. Run `pytest -m auth -v` and confirm all 11 tests in `tests/api/test_auth_api.py` pass.
2. Add a test that asserts the error message body differs between 401 (missing key) and 403 (wrong key).
3. Add a test that verifies the `X-API-Key` header is **not** required on `GET /api/orders` and `GET /api/orders/stats`.

**Hints:** Use `res.get_json()["error"]` to read the error message.

**Done when:** `pytest -m auth -v` is fully green; new tests pass.

---

## Task 10: Filtering and Pagination Tests (Day 10)

**Training Plan:** [→ Day 10: Filtering, Pagination, and Stats Tests](training_plan.md#day-10-filtering-pagination-and-stats-tests)

**Goal:** Test all query parameters on `GET /api/orders`.

**Steps:**
1. Add a test that creates 7 orders and checks `pages == 3` when `limit == 3`.
2. Add a test that combines `?customer=Alice&status=pending` and asserts only Alice's pending orders are returned.
3. Add a test for `?sort=price_desc` with 3 orders at different prices.
4. Run `pytest -m api -v` — all tests pass.

**Done when:** All new filter/pagination tests pass; existing tests are unchanged.

---

## Task 11: Selenium Basics (Day 11)

**Training Plan:** [→ Day 11: Selenium Basics and Explicit Waits](training_plan.md#day-11-selenium-basics-and-explicit-waits)

**Goal:** Understand the Selenium test setup and write an explicit-wait test.

**Steps:**
1. Run `pytest -m ui -v` — all 4 existing tests must pass.
2. Write `test_order_count_increases` in `tests/ui/test_orders_ui.py` that:
   - Creates two orders via the UI.
   - Uses `WebDriverWait` to wait until the table body has ≥ 2 rows.
   - Asserts `len(page.get_order_rows()) >= 2`.
3. Confirm no `time.sleep` is used anywhere in the test file.

**Done when:** `pytest -m ui -v` shows 5 green tests; no `sleep` calls.

---

## Task 12: Page Object Model (Day 12)

**Training Plan:** [→ Day 12: Page Object Model](training_plan.md#day-12-page-object-model)

**Goal:** Extend `OrderPage` and write tests that use it exclusively.

**Steps:**
1. Add `get_error_message(self) -> str` to `tests/ui/pages/order_page.py` that returns the text of `#error-msg`.
2. Write `test_empty_form_shows_error` in `tests/ui/test_orders_ui.py` that clicks Add Order on an empty form and asserts the error message is not empty.
3. Add a `filter_by_status` test using `OrderPage.filter_by_status("fulfilled")`.
4. Verify no `find_element` calls appear outside `order_page.py`.

**Done when:** All new UI tests pass; POM encapsulates all locators.

---

## Task 13: Screenshot on Failure (Day 13)

**Training Plan:** [→ Day 13: Screenshot on Failure and Advanced UI Testing](training_plan.md#day-13-screenshot-on-failure-and-advanced-ui-testing)

**Goal:** Understand and verify the screenshot hook.

**Steps:**
1. Temporarily change a locator in `test_create_order_via_ui` to something invalid (e.g., `By.ID, "nonexistent"`).
2. Run `pytest -m ui -v` and observe the failure.
3. Confirm a `.png` file appears in `reports/screenshots/`.
4. Revert the change and confirm the screenshot is no longer saved.

**Done when:** Screenshot is saved on failure; none saved on pass; broken locator reverted.

---

## Task 14: Coverage and HTML Reports (Day 14)

**Training Plan:** [→ Day 14: Coverage, HTML Reports, and Code Quality](training_plan.md#day-14-coverage-html-reports-and-code-quality)

**Goal:** Measure coverage and reach ≥ 80% on `src/`.

**Steps:**
1. Run `pytest -m api --cov=src --cov-report=term-missing`.
2. Identify at least 2 uncovered lines in the output.
3. Write tests that cover those lines.
4. Re-run and confirm coverage ≥ 80%.
5. Open `reports/report.html` in a browser.
6. Run `black --check .` and fix any violations.

**Done when:** Coverage ≥ 80%; HTML report opens; `black --check .` exits 0.

---

## Task 15: CI/CD and Interview Prep (Day 15)

**Training Plan:** [→ Day 15: CI/CD Deep Dive and Interview Prep](training_plan.md#day-15-cicd-deep-dive-and-interview-prep)

**Goal:** Operate the full CI pipeline and consolidate interview readiness.

**Steps:**
1. Create a branch `feature/day15-ci-practice`.
2. Introduce a deliberate test failure, push, and observe the CI failure in the Actions tab.
3. Fix the failure and push again — CI must go green.
4. Read and answer every question in [Interview Prep](interview_prep.md) (write answers in `scratch/day15_interview.md`).
5. Write 2–3 resume bullet-point sentences describing this project.

**Done when:** CI is green; answers file exists; resume bullets written.

---

## Related Guides

- [Onboarding](onboarding.md) — environment setup
- [Learning Path](learning_path.md) — phase-by-phase progression
- [Training Plan](training_plan.md) — structured daily schedule
- [Development Guide](development_guide.md) — branching and test workflow
- [Best Practices](best_practices.md) — automation patterns and checklist
- [Contributing](../CONTRIBUTING.md) — PR and commit conventions
