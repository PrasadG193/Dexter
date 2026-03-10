# Learning Path

This path guides you from Python fundamentals to automation-ready SDET skills by building and testing the Order Board project end-to-end.

> **New to the project?** Start with the [Onboarding Guide](onboarding.md) to set up your environment first.
> See also: [Training Plan](training_plan.md) for a day-by-day schedule and [Development Guide](development_guide.md) for branching workflow.

---

## Phase 1: Python Foundations (Days 1–5)

1. Data types: `str`, `int`, `float`, `list`, `dict`, `set`, `tuple`
2. List/dict comprehensions and functional tools (`map`, `filter`)
3. Functions, type hints, default arguments, modules
4. Error handling: `try/except/finally`, custom exceptions
5. OOP and `@dataclass` — read `src/models.py`
6. Flask basics: routes, request/response, JSON, HTTP status codes

**Outcome:** You can read and write small Python scripts, understand the Order Board app, and call every endpoint with curl.

**Key files:** `src/models.py`, `src/utils.py`, `src/app.py`, `data/sample_orders.json`

---

## Phase 2: API Test Automation (Days 6–10)

1. `pytest` fundamentals: fixtures, assertions, `conftest.py`, fixture scope
2. Parametrized tests with `@pytest.mark.parametrize`
3. Test data management: fixture factories, JSON data files
4. Authentication testing: 401 vs. 403, header-based auth
5. Advanced query testing: filtering, pagination, aggregate endpoints, `pytest.approx`

**Outcome:** You can design and automate a complete API test suite — positive, negative, parametrized, and auth tests — and run it with a single `pytest -m api -v` command.

**Key files:** `tests/conftest.py`, `tests/api/test_orders_api.py`, `tests/api/test_filters_api.py`, `tests/api/test_auth_api.py`

---

## Phase 3: UI Automation + CI/CD (Days 11–15)

1. Selenium WebDriver: setup, locators, `WebDriverWait` with `ExpectedConditions`
2. Page Object Model: encapsulate locators and actions in `OrderPage`
3. Advanced UI: filter tests, stats panel, screenshot on failure
4. Coverage and reporting: `pytest-cov`, `pytest-html`, `black`
5. CI/CD: GitHub Actions, workflow triggers, artifact upload, debugging failures

**Outcome:** You can write maintainable UI automation using POM, measure and improve test coverage, and operate a CI pipeline from end to end.

**Key files:** `tests/ui/pages/order_page.py`, `tests/ui/test_orders_ui.py`, `.github/workflows/ci.yml`

---

## Skills Checklist

After completing all three phases you should be able to:

- [ ] Write Python with type hints, error handling, and dataclasses
- [ ] Build and test REST API endpoints with Flask and pytest
- [ ] Use `@pytest.mark.parametrize` for data-driven tests
- [ ] Test API authentication (401, 403 scenarios)
- [ ] Test filtering, pagination, and aggregate endpoints
- [ ] Write Selenium UI tests using the Page Object Model
- [ ] Use `WebDriverWait` (never `time.sleep`)
- [ ] Capture screenshots on test failure automatically
- [ ] Generate HTML test reports with `pytest-html`
- [ ] Measure code coverage with `pytest-cov`
- [ ] Operate and debug a GitHub Actions CI pipeline
- [ ] Apply `black` code formatting

---

## Related Guides

- [Onboarding](onboarding.md) — environment setup
- [Training Plan](training_plan.md) — structured 15-day daily schedule
- [Hands-on Tasks](tasks.md) — incremental coding tasks
- [Best Practices](best_practices.md) — automation patterns and checklist
- [Interview Prep](interview_prep.md) — 30+ interview Q&As
- [Development Guide](development_guide.md) — branching and test workflow
- [CI/CD Guide](ci_cd.md) — GitHub Actions details
