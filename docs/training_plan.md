# Training Plan

A structured 2-week plan for automation engineers learning Python SDET skills with the Dexter project.

---

## Overview

| Week | Focus | Goal |
|------|-------|------|
| Week 1 | Python foundations + project setup | Write and run basic Python; understand the app |
| Week 2 | Automation deep dive + CI/CD | Build a full test suite; operate CI pipeline |

---

## Week 1 — Foundations

### Day 1: Python Basics

**Topics:** Data types, variables, operators, collections (list, dict, set, tuple), control flow.

**Exercises:**
- [ ] Write a script that creates a list of 5 sample orders (dicts) and prints each one.
- [ ] Filter orders where `qty > 1` using a list comprehension.
- [ ] Write a function `calculate_total(price, qty)` that returns the total cost.

**Deliverable:** `scratch/day1_basics.py` with the above exercises.

---

### Day 2: Functions, Modules, and Error Handling

**Topics:** Functions, modules, imports, exceptions, logging.

**Exercises:**
- [ ] Refactor `calculate_total` into a new module `src/utils.py`.
- [ ] Add input validation that raises `ValueError` for negative price or zero quantity.
- [ ] Write a test in `tests/api/` that calls the validation logic and asserts the error.

**Deliverable:** Updated `src/utils.py` and a passing test.

---

### Day 3: Project Setup and App Exploration

**Topics:** Virtual environments, pip, Flask basics, REST concepts.

**Exercises:**
- [ ] Complete [Onboarding Guide](onboarding.md) setup from scratch.
- [ ] Start the app and use `curl` to call each API endpoint.
- [ ] Read `src/app.py` and `src/data_store.py` and describe (in comments) what each function does.

**Deliverable:** Running app with annotated source code comments.

---

### Day 4: First API Tests

**Topics:** `pytest` basics, fixtures, assertions, HTTP status codes.

**Exercises:**
- [ ] Read `tests/api/test_orders_api.py`.
- [ ] Add tests for: create with missing fields (400), create with invalid price (400), fetch a nonexistent order (404).
- [ ] Run `pytest -m api -v` and confirm all pass.

**Deliverable:** At least 3 new passing API tests.

---

### Day 5: Deeper API Testing

**Topics:** Parametrize, negative testing, boundary conditions.

**Exercises:**
- [ ] Use `@pytest.mark.parametrize` to test 4–5 invalid payloads in a single test function.
- [ ] Add a test that creates 3 orders and asserts the list endpoint returns all 3.
- [ ] Add a test for the update endpoint (PUT).

**Deliverable:** Parametrized test block + update/list test.

---

## Week 2 — Automation and CI/CD

### Day 6: Selenium UI Basics

**Topics:** WebDriver setup, locators, explicit waits, Page Object basics.

**Exercises:**
- [ ] Read `tests/ui/test_orders_ui.py`.
- [ ] Add a test that creates an order through the UI and verifies it appears in the list.
- [ ] Replace any `time.sleep` calls (if present) with `WebDriverWait`.

**Deliverable:** 1 new UI test using explicit waits.

---

### Day 7: Advanced UI Testing

**Topics:** Form validation, error messages, dynamic content.

**Exercises:**
- [ ] Add a test that submits an empty form and asserts a validation message appears.
- [ ] Add a test that deletes an order through the UI and verifies it is removed.
- [ ] Introduce a simple Page Object for the Order Board page.

**Deliverable:** 2 new UI tests + a Page Object class.

---

### Day 8: Code Quality

**Topics:** `black` formatting, naming conventions, code review.

**Exercises:**
- [ ] Run `black --check .` and fix any violations.
- [ ] Review your test code against the [Best Practices](best_practices.md) checklist.
- [ ] Open a PR for your week's work and complete the PR checklist in [CONTRIBUTING.md](../CONTRIBUTING.md).

**Deliverable:** Formatted, reviewed PR.

---

### Day 9: CI/CD

**Topics:** GitHub Actions, workflow YAML, reading logs.

**Exercises:**
- [ ] Read [CI/CD Guide](ci_cd.md) and `.github/workflows/ci.yml`.
- [ ] Push a branch and watch the workflow run in the Actions tab.
- [ ] Intentionally break a test, push, observe the failure in CI, then fix it.
- [ ] Add a CI status badge to your fork's README.

**Deliverable:** PR with a green CI run.

---

### Day 10: Interview Prep and Review

**Topics:** Consolidation, reflection, mock interview prep.

**Exercises:**
- [ ] Review all completed tasks against [tasks.md](tasks.md).
- [ ] Work through the interview prep checklist below.
- [ ] Write 2–3 sentences describing the project for a resume bullet point.

**Deliverable:** Completed interview prep checklist.

---

## Interview Prep Checklist

Use this checklist to self-assess before a Python SDET interview.

### Python

- [ ] Explain the difference between a list and a tuple; give an automation use case for each.
- [ ] Write a function that reads a JSON file and returns a list of dicts.
- [ ] Describe what a decorator is and name two used in `pytest`.

### API Automation

- [ ] Explain what `pytest` fixtures are and give an example.
- [ ] Describe how you would test a paginated API endpoint.
- [ ] What is the difference between a 400 and a 422 status code?
- [ ] How do you handle authentication tokens in API tests?

### UI Automation (Selenium)

- [ ] What is the difference between implicit and explicit waits?
- [ ] Describe the Page Object Model (POM) pattern.
- [ ] How would you handle a dynamically loaded table in Selenium?
- [ ] What causes flaky UI tests and how do you reduce them?

### CI/CD

- [ ] Describe the steps in the GitHub Actions workflow for this project.
- [ ] How would you run only API tests in CI (not UI tests)?
- [ ] What is the purpose of a `requirements.txt` file?

### Soft Skills

- [ ] How do you decide which tests to automate versus test manually?
- [ ] Describe a time a test caught a real bug.
- [ ] How do you keep a test suite maintainable as the application grows?

---

## Expected Outcomes

By the end of the two-week plan you should be able to:

1. Write Python functions with proper error handling and logging.
2. Design and implement REST API tests with `pytest`, covering positive and negative cases.
3. Write UI tests with Selenium using explicit waits and a basic Page Object pattern.
4. Run, read, and debug a GitHub Actions CI workflow.
5. Apply code formatting (`black`) and follow commit conventions.
6. Confidently answer common Python SDET interview questions.

---

## Related Guides

- [Onboarding](onboarding.md) — environment setup
- [Learning Path](learning_path.md) — phase-by-phase progression
- [Hands-on Tasks](tasks.md) — task list
- [Best Practices](best_practices.md) — automation patterns
- [Development Guide](development_guide.md) — branching and workflow
