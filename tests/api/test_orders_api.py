"""API tests for Order Board."""

import pytest

SAMPLE = {"customer": "Alice", "item": "Widget", "quantity": 2, "price": 9.99}


@pytest.mark.api
def test_health(client):
    res = client.get("/api/health")
    assert res.status_code == 200
    assert res.get_json() == {"status": "ok"}


@pytest.mark.api
def test_list_orders_empty(client):
    res = client.get("/api/orders")
    assert res.status_code == 200
    assert res.get_json() == {"orders": []}


@pytest.mark.api
def test_create_order(client, auth_headers):
    res = client.post("/api/orders", json=SAMPLE, headers=auth_headers)
    assert res.status_code == 201
    data = res.get_json()
    assert data["customer"] == "Alice"
    assert data["item"] == "Widget"
    assert data["quantity"] == 2
    assert data["price"] == 9.99
    assert "id" in data
    assert data["status"] == "pending"


@pytest.mark.api
def test_create_order_missing_field(client, auth_headers):
    res = client.post("/api/orders", json={"customer": "Bob"}, headers=auth_headers)
    assert res.status_code == 400
    assert "error" in res.get_json()


@pytest.mark.api
@pytest.mark.parametrize(
    "payload",
    [
        {"customer": "X", "item": "Y", "quantity": 2},  # missing price
        {"customer": "X", "item": "Y", "price": 5.0},  # missing quantity
        {"customer": "X", "item": "Y", "quantity": 0, "price": 5.0},  # zero qty
        {"customer": "X", "item": "Y", "quantity": 2, "price": -1.0},  # negative price
        {"customer": "X", "item": "Y", "quantity": "two", "price": 5.0},  # wrong type
    ],
)
def test_create_order_invalid_payload(client, auth_headers, payload):
    res = client.post("/api/orders", json=payload, headers=auth_headers)
    assert res.status_code == 400
    assert "error" in res.get_json()


@pytest.mark.api
def test_get_order(client, auth_headers):
    create_res = client.post("/api/orders", json=SAMPLE, headers=auth_headers)
    order_id = create_res.get_json()["id"]
    res = client.get(f"/api/orders/{order_id}")
    assert res.status_code == 200
    assert res.get_json()["id"] == order_id


@pytest.mark.api
def test_get_order_not_found(client):
    res = client.get("/api/orders/nonexistent-id")
    assert res.status_code == 404


@pytest.mark.api
def test_update_order(client, auth_headers):
    order_id = client.post("/api/orders", json=SAMPLE, headers=auth_headers).get_json()[
        "id"
    ]
    res = client.put(
        f"/api/orders/{order_id}", json={"status": "fulfilled"}, headers=auth_headers
    )
    assert res.status_code == 200
    assert res.get_json()["status"] == "fulfilled"


@pytest.mark.api
def test_update_order_not_found(client, auth_headers):
    res = client.put(
        "/api/orders/nonexistent-id", json={"status": "fulfilled"}, headers=auth_headers
    )
    assert res.status_code == 404


@pytest.mark.api
def test_update_order_invalid_transition(client, auth_headers):
    order_id = client.post("/api/orders", json=SAMPLE, headers=auth_headers).get_json()[
        "id"
    ]
    client.put(
        f"/api/orders/{order_id}", json={"status": "fulfilled"}, headers=auth_headers
    )
    res = client.put(
        f"/api/orders/{order_id}", json={"status": "pending"}, headers=auth_headers
    )
    assert res.status_code == 400
    assert "transition" in res.get_json()["error"].lower()


@pytest.mark.api
def test_delete_order(client, auth_headers):
    order_id = client.post("/api/orders", json=SAMPLE, headers=auth_headers).get_json()[
        "id"
    ]
    res = client.delete(f"/api/orders/{order_id}", headers=auth_headers)
    assert res.status_code == 200
    assert res.get_json()["deleted"] == order_id
    assert client.get(f"/api/orders/{order_id}").status_code == 404


@pytest.mark.api
def test_delete_order_not_found(client, auth_headers):
    res = client.delete("/api/orders/nonexistent-id", headers=auth_headers)
    assert res.status_code == 404


@pytest.mark.api
def test_orders_sorted_by_created_at(client, auth_headers):
    client.post(
        "/api/orders", json={**SAMPLE, "customer": "First"}, headers=auth_headers
    )
    client.post(
        "/api/orders", json={**SAMPLE, "customer": "Second"}, headers=auth_headers
    )
    orders = client.get("/api/orders").get_json()["orders"]
    assert len(orders) == 2
    assert orders[0]["created_at"] <= orders[1]["created_at"]
