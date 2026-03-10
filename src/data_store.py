"""In-memory Order store."""

from dataclasses import asdict

from src.models import Order

_orders: dict[str, Order] = {}


def create_order(customer: str, item: str, quantity: int, price: float) -> Order:
    order = Order(customer=customer, item=item, quantity=quantity, price=price)
    _orders[order.id] = order
    return order


def get_all_orders() -> list[Order]:
    return sorted(_orders.values(), key=lambda o: o.created_at)


def get_order(order_id: str) -> Order | None:
    return _orders.get(order_id)


def update_order(order_id: str, **kwargs) -> Order | None:
    order = _orders.get(order_id)
    if order is None:
        return None
    for key, value in kwargs.items():
        if hasattr(order, key) and key not in ("id", "created_at"):
            setattr(order, key, value)
    return order


def delete_order(order_id: str) -> bool:
    if order_id in _orders:
        del _orders[order_id]
        return True
    return False


def clear_orders() -> None:
    """Remove all orders (used in tests)."""
    _orders.clear()


def filter_orders(
    status: str | None = None,
    customer: str | None = None,
    sort_by: str | None = None,
) -> list[Order]:
    """Return filtered and sorted list of orders."""
    orders = get_all_orders()
    if status:
        orders = [o for o in orders if o.status == status]
    if customer:
        orders = [o for o in orders if customer.lower() in o.customer.lower()]
    if sort_by == "price":
        orders = sorted(orders, key=lambda o: o.price)
    elif sort_by == "price_desc":
        orders = sorted(orders, key=lambda o: o.price, reverse=True)
    return orders


def order_to_dict(order: Order) -> dict:
    return asdict(order)
