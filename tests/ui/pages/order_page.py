"""Page Object Model for the Order Board page."""

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait


class OrderPage:
    """Encapsulates all interactions with the Order Board UI."""

    URL_PATH = "/"
    WAIT_TIMEOUT = 10

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, self.WAIT_TIMEOUT)

    def open(self, base_url: str) -> "OrderPage":
        """Navigate to the Order Board page."""
        self.driver.get(base_url + self.URL_PATH)
        return self

    def create_order(
        self, customer: str, item: str, qty: str, price: str
    ) -> "OrderPage":
        """Fill in the order form and submit it, then wait for the row to appear."""
        self.driver.find_element(By.ID, "customer").clear()
        self.driver.find_element(By.ID, "customer").send_keys(customer)
        self.driver.find_element(By.ID, "item").clear()
        self.driver.find_element(By.ID, "item").send_keys(item)
        self.driver.find_element(By.ID, "quantity").clear()
        self.driver.find_element(By.ID, "quantity").send_keys(qty)
        self.driver.find_element(By.ID, "price").clear()
        self.driver.find_element(By.ID, "price").send_keys(price)
        self.driver.find_element(By.ID, "add-btn").click()
        self.wait.until(
            EC.text_to_be_present_in_element((By.ID, "orders-body"), customer)
        )
        return self

    def get_order_rows(self) -> list:
        """Return all rows currently visible in the orders table."""
        return self.driver.find_elements(By.CSS_SELECTOR, "#orders-body tr")

    def delete_order_by_customer(self, customer: str) -> "OrderPage":
        """Click the Delete button on the first row matching the given customer name."""
        rows = self.get_order_rows()
        for row in rows:
            if customer in row.text:
                row.find_element(By.CSS_SELECTOR, ".del-btn").click()
                break
        self.wait.until(
            lambda d: customer not in d.find_element(By.ID, "orders-body").text
        )
        return self

    def filter_by_status(self, status: str) -> "OrderPage":
        """Select a status from the filter dropdown (use '' for 'All')."""
        Select(self.driver.find_element(By.ID, "status-filter")).select_by_value(status)
        return self

    def get_stats(self) -> dict:
        """Return the current values shown in the stats panel."""
        return {
            "total": self.driver.find_element(By.ID, "stats-total").text,
            "revenue": self.driver.find_element(By.ID, "stats-revenue").text,
            "pending": self.driver.find_element(By.ID, "stats-pending").text,
            "fulfilled": self.driver.find_element(By.ID, "stats-fulfilled").text,
            "cancelled": self.driver.find_element(By.ID, "stats-cancelled").text,
        }
