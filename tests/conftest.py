"""Shared pytest fixtures."""

import json
import os

import pytest

from src.app import app as flask_app
from src.data_store import clear_orders


@pytest.fixture()
def client():
    flask_app.config["TESTING"] = True
    with flask_app.test_client() as client:
        yield client
    clear_orders()


@pytest.fixture()
def auth_headers():
    """API key header required for mutating endpoints."""
    return {"X-API-Key": "secret"}


@pytest.fixture()
def order_payload():
    """Factory fixture that returns a valid order dict."""

    def _make(customer="Alice", item="Widget", quantity=2, price=9.99):
        return {
            "customer": customer,
            "item": item,
            "quantity": quantity,
            "price": price,
        }

    return _make


@pytest.fixture()
def sample_orders(client, auth_headers):
    """Create 5 orders from data/sample_orders.json and yield the created list."""
    data_file = os.path.join(
        os.path.dirname(__file__), "..", "data", "sample_orders.json"
    )
    with open(data_file) as f:
        payloads = json.load(f)
    created = []
    for payload in payloads:
        res = client.post("/api/orders", json=payload, headers=auth_headers)
        created.append(res.get_json())
    yield created
    clear_orders()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Capture a screenshot on UI test failure."""
    outcome = yield
    rep = outcome.get_result()
    if rep.when == "call" and rep.failed:
        driver = item.funcargs.get("driver")
        if driver is not None:
            screenshots_dir = os.path.join(
                os.path.dirname(__file__), "..", "reports", "screenshots"
            )
            os.makedirs(screenshots_dir, exist_ok=True)
            safe_name = item.nodeid.replace("/", "_").replace("::", "_")
            path = os.path.join(screenshots_dir, f"{safe_name}.png")
            driver.save_screenshot(path)
