# Learning Path

This path guides you from Python fundamentals to automation-ready skills by building the Order Board project end-to-end.

> **New to the project?** Start with the [Onboarding Guide](onboarding.md) to set up your environment first.
> See also: [Training Plan](training_plan.md) for a structured daily schedule, and [Development Guide](development_guide.md) for branching and test workflow.

## Phase 1: Python Foundations (Day 1-2)
1. Data types, variables, and operators
2. Collections: list, dict, set, tuple
3. Control flow: if/else, loops
4. Functions and modules
5. Exceptions and logging

**Outcome:** You can read/write small Python scripts and understand basic syntax.

## Phase 2: Project Core (Day 3-4)
1. Read `src/data_store.py` to understand how in-memory data is handled.
2. Run the Flask app (`python -m src.app`).
3. Use curl or Postman to hit `/api/orders` and `/api/health`.

**Outcome:** You understand the basic API and how it stores data.

## Phase 3: API Automation (Day 5-6)
1. Read `tests/api/test_orders_api.py`.
2. Add more tests for negative cases and validation.
3. Add new API features and write tests first (TDD style).

**Outcome:** You can design and automate API tests with pytest.

## Phase 4: UI Automation (Day 7)
1. Review `tests/ui/test_orders_ui.py`.
2. Add new UI validations (edge cases, error handling).
3. Add a new UI feature and automate it.

**Outcome:** You can run UI automation with Selenium.

## Phase 5: CI/CD (Day 8)
1. Read `docs/ci_cd.md`.
2. Trigger GitHub Actions by pushing a change.
3. Inspect the workflow logs and artifacts.

**Outcome:** You can operate a CI pipeline for automated tests.

---

## Related Guides

- [Onboarding](onboarding.md) — environment setup
- [Training Plan](training_plan.md) — structured daily schedule
- [Hands-on Tasks](tasks.md) — incremental coding tasks
- [Best Practices](best_practices.md) — automation patterns and checklist
- [Development Guide](development_guide.md) — branching and test workflow
- [CI/CD Guide](ci_cd.md) — GitHub Actions details