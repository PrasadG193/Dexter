"""UI tests for Order Board (Selenium)."""

import threading
import time

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from src.app import app as flask_app
from src.data_store import clear_orders
from tests.ui.pages.order_page import OrderPage

HOST = "127.0.0.1"
PORT = 5099


@pytest.fixture(scope="module")
def live_server():
    """Start Flask in a background thread for Selenium tests."""
    clear_orders()
    server = threading.Thread(
        target=lambda: flask_app.run(host=HOST, port=PORT, use_reloader=False),
        daemon=True,
    )
    server.start()
    time.sleep(1)
    yield f"http://{HOST}:{PORT}"
    clear_orders()


@pytest.fixture()
def driver():
    opts = Options()
    opts.add_argument("--headless")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    drv = webdriver.Chrome(options=opts)
    yield drv
    drv.quit()


@pytest.mark.ui
def test_page_title(driver, live_server):
    OrderPage(driver).open(live_server)
    assert "Order Board" in driver.title


@pytest.mark.ui
def test_create_order_via_ui(driver, live_server):
    clear_orders()
    page = OrderPage(driver)
    page.open(live_server)
    page.create_order("UIUser", "Gadget", "3", "19.99")
    rows = page.get_order_rows()
    assert any("UIUser" in r.text for r in rows)


@pytest.mark.ui
def test_delete_order_via_ui(driver, live_server):
    clear_orders()
    page = OrderPage(driver)
    page.open(live_server)
    page.create_order("ToDelete", "Thing", "1", "5.00")
    page.delete_order_by_customer("ToDelete")
    rows = page.get_order_rows()
    assert all("ToDelete" not in r.text for r in rows)


@pytest.mark.ui
def test_stats_panel_shows_totals(driver, live_server):
    clear_orders()
    page = OrderPage(driver)
    page.open(live_server)
    page.create_order("StatsUser", "Item", "2", "10.00")
    wait = WebDriverWait(driver, 10)
    wait.until(lambda d: d.find_element(By.ID, "stats-total").text != "0")
    stats = page.get_stats()
    assert stats["total"] == "1"
    assert stats["pending"] == "1"
