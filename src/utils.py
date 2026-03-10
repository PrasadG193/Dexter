"""Helper functions for Order Board."""


def validate_order_payload(data: dict) -> list[str]:
    """Return list of validation error messages for an order payload."""
    errors: list[str] = []
    for field in ("customer", "item", "quantity", "price"):
        if field not in data:
            errors.append(f"Missing required field: {field}")
    if "price" in data:
        try:
            if float(data["price"]) < 0:
                errors.append("price must be non-negative")
        except (TypeError, ValueError):
            errors.append("price must be a number")
    if "quantity" in data:
        try:
            if int(data["quantity"]) < 1:
                errors.append("quantity must be at least 1")
        except (TypeError, ValueError):
            errors.append("quantity must be an integer")
    return errors


def format_price(price: float) -> str:
    """Format a price as a dollar string, e.g. '$9.99'."""
    return f"${price:.2f}"


def calculate_order_total(orders: list[dict]) -> float:
    """Return sum of price * quantity for all orders."""
    return sum(o.get("price", 0) * o.get("quantity", 0) for o in orders)
