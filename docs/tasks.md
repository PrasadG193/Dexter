# Hands-on Tasks

Each task builds Python fundamentals and automation skills. Start with Task 1 and proceed sequentially.

## Task 1: Python Basics
- Print a welcome banner and current date.
- Read user input for name and display a greeting.
- Store 3 sample orders in a list of dictionaries.

## Task 2: Functions and Modules
- Create a function `calculate_total(price, qty)`.  
- Add a function to generate a new order ID.    
- Export functions from a new module `src/utils.py`.

## Task 3: Error Handling
- Add validation for missing fields in the API (return 400 with a message).
- Write a test that asserts the error response.

## Task 4: Data Manipulation
- Add sorting by `created_at` to the `/api/orders` endpoint.
- Add a test to confirm sorting.

## Task 5: API Automation (pytest)
- Add a test for updating an order.
- Add a test for deleting an order.
- Add a test for invalid ID handling.

## Task 6: UI Automation (Selenium)
- Add a test that creates a new order through the UI.
- Add a test that deletes an order through the UI.
- Add a test that checks UI validation messages.

## Task 7: CI/CD
- Update the GitHub Actions workflow to include `pytest -m api`.
- Add a badge to the README after CI passes.

## Task 8: Real-world Practices
- Add a `CHANGELOG.md` entry for new features.
- Add `CONTRIBUTING.md` with run instructions.
- Add code formatting via `black` and a CI step.