"""Flask Order Board application."""

import os

from flask import Flask, jsonify, request, render_template

from src.data_store import (
    create_order,
    get_all_orders,
    get_order,
    update_order,
    delete_order,
    filter_orders,
    order_to_dict,
)
from src.models import STATUS_TRANSITIONS, VALID_STATUSES
from src.utils import validate_order_payload

app = Flask(__name__)

API_KEY = os.environ.get("API_KEY", "secret")
_MUTATING_METHODS = {"POST", "PUT", "DELETE"}


@app.before_request
def require_api_key():
    """Enforce API key for all mutating API endpoints."""
    if request.method in _MUTATING_METHODS and request.path.startswith("/api/"):
        key = request.headers.get("X-API-Key")
        if key is None:
            return jsonify({"error": "Missing X-API-Key header"}), 401
        if key != API_KEY:
            return jsonify({"error": "Invalid API key"}), 403


@app.get("/api/health")
def health():
    return jsonify({"status": "ok"})


@app.get("/api/orders/stats")
def order_stats():
    orders = get_all_orders()
    by_status = {s: sum(1 for o in orders if o.status == s) for s in VALID_STATUSES}
    revenue = sum(o.price * o.quantity for o in orders)
    return jsonify(
        {
            "total": len(orders),
            "revenue": round(revenue, 2),
            "by_status": by_status,
        }
    )


@app.get("/api/orders")
def list_orders():
    status = request.args.get("status")
    customer = request.args.get("customer")
    sort_by = request.args.get("sort")
    page = int(request.args.get("page", 1))
    limit = int(request.args.get("limit", 0))

    orders = filter_orders(status=status, customer=customer, sort_by=sort_by)
    total = len(orders)

    if limit > 0:
        pages = (total + limit - 1) // limit
        start = (page - 1) * limit
        orders = orders[start : start + limit]
        return jsonify(
            {
                "orders": [order_to_dict(o) for o in orders],
                "total": total,
                "page": page,
                "pages": pages,
            }
        )

    return jsonify({"orders": [order_to_dict(o) for o in orders]})


@app.post("/api/orders")
def add_order():
    data = request.get_json(silent=True) or {}
    errors = validate_order_payload(data)
    if errors:
        return jsonify({"error": errors[0]}), 400
    order = create_order(
        customer=data["customer"],
        item=data["item"],
        quantity=data["quantity"],
        price=data["price"],
    )
    return jsonify(order_to_dict(order)), 201


@app.get("/api/orders/<order_id>")
def get_one_order(order_id: str):
    order = get_order(order_id)
    if order is None:
        return jsonify({"error": "Order not found"}), 404
    return jsonify(order_to_dict(order))


@app.put("/api/orders/<order_id>")
def update_one_order(order_id: str):
    data = request.get_json(silent=True) or {}
    order = get_order(order_id)
    if order is None:
        return jsonify({"error": "Order not found"}), 404
    new_status = data.get("status")
    if new_status is not None and new_status != order.status:
        allowed = STATUS_TRANSITIONS.get(order.status, set())
        if new_status not in allowed:
            return (
                jsonify(
                    {
                        "error": f"Invalid status transition: {order.status} → {new_status}"
                    }
                ),
                400,
            )
    order = update_order(order_id, **data)
    return jsonify(order_to_dict(order))


@app.delete("/api/orders/<order_id>")
def delete_one_order(order_id: str):
    if not delete_order(order_id):
        return jsonify({"error": "Order not found"}), 404
    return jsonify({"deleted": order_id})


@app.get("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
