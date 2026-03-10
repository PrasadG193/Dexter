"""API tests for filtering, sorting, pagination, and stats."""

import pytest

SAMPLE = {"customer": "Alice", "item": "Widget", "quantity": 2, "price": 9.99}


@pytest.mark.api
def test_filter_by_status(client, auth_headers):
    client.post("/api/orders", json=SAMPLE, headers=auth_headers)
    order_id = client.post(
        "/api/orders", json={**SAMPLE, "customer": "Bob"}, headers=auth_headers
    ).get_json()["id"]
    client.put(
        f"/api/orders/{order_id}", json={"status": "fulfilled"}, headers=auth_headers
    )

    res = client.get("/api/orders?status=pending")
    orders = res.get_json()["orders"]
    assert all(o["status"] == "pending" for o in orders)
    assert len(orders) == 1


@pytest.mark.api
def test_filter_by_customer(client, auth_headers):
    client.post("/api/orders", json=SAMPLE, headers=auth_headers)
    client.post("/api/orders", json={**SAMPLE, "customer": "Bob"}, headers=auth_headers)

    res = client.get("/api/orders?customer=alice")
    orders = res.get_json()["orders"]
    assert len(orders) == 1
    assert orders[0]["customer"] == "Alice"


@pytest.mark.api
def test_sort_by_price_ascending(client, auth_headers):
    for price in (20.00, 5.00, 15.00):
        client.post(
            "/api/orders", json={**SAMPLE, "price": price}, headers=auth_headers
        )

    orders = client.get("/api/orders?sort=price").get_json()["orders"]
    prices = [o["price"] for o in orders]
    assert prices == sorted(prices)


@pytest.mark.api
def test_sort_by_price_descending(client, auth_headers):
    for price in (20.00, 5.00, 15.00):
        client.post(
            "/api/orders", json={**SAMPLE, "price": price}, headers=auth_headers
        )

    orders = client.get("/api/orders?sort=price_desc").get_json()["orders"]
    prices = [o["price"] for o in orders]
    assert prices == sorted(prices, reverse=True)


@pytest.mark.api
def test_pagination_page_1(client, auth_headers):
    for i in range(5):
        client.post(
            "/api/orders",
            json={**SAMPLE, "customer": f"Customer{i}"},
            headers=auth_headers,
        )

    data = client.get("/api/orders?page=1&limit=3").get_json()
    assert len(data["orders"]) == 3
    assert data["total"] == 5
    assert data["page"] == 1
    assert data["pages"] == 2


@pytest.mark.api
def test_pagination_page_2(client, auth_headers):
    for i in range(5):
        client.post(
            "/api/orders",
            json={**SAMPLE, "customer": f"Customer{i}"},
            headers=auth_headers,
        )

    data = client.get("/api/orders?page=2&limit=3").get_json()
    assert len(data["orders"]) == 2
    assert data["total"] == 5
    assert data["pages"] == 2


@pytest.mark.api
def test_stats_total_and_revenue(client, auth_headers):
    client.post(
        "/api/orders",
        json={**SAMPLE, "quantity": 1, "price": 10.00},
        headers=auth_headers,
    )
    order_id = client.post(
        "/api/orders",
        json={**SAMPLE, "quantity": 2, "price": 5.00},
        headers=auth_headers,
    ).get_json()["id"]
    client.put(
        f"/api/orders/{order_id}", json={"status": "fulfilled"}, headers=auth_headers
    )

    data = client.get("/api/orders/stats").get_json()
    assert data["total"] == 2
    assert data["revenue"] == pytest.approx(20.00)
    assert data["by_status"]["pending"] == 1
    assert data["by_status"]["fulfilled"] == 1
    assert data["by_status"]["cancelled"] == 0


@pytest.mark.api
def test_stats_empty(client):
    data = client.get("/api/orders/stats").get_json()
    assert data["total"] == 0
    assert data["revenue"] == 0.0


@pytest.mark.api
def test_sample_orders_fixture(sample_orders):
    """Verify the sample_orders fixture loads all 5 orders."""
    assert len(sample_orders) == 5
    customers = {o["customer"] for o in sample_orders}
    assert "Alice" in customers
    assert "Dave" in customers
