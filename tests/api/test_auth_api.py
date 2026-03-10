"""Authentication tests for Order Board API."""

import pytest

SAMPLE = {"customer": "Alice", "item": "Widget", "quantity": 2, "price": 9.99}


@pytest.mark.auth
def test_post_without_api_key_returns_401(client):
    res = client.post("/api/orders", json=SAMPLE)
    assert res.status_code == 401
    assert "error" in res.get_json()


@pytest.mark.auth
def test_post_with_wrong_api_key_returns_403(client):
    res = client.post("/api/orders", json=SAMPLE, headers={"X-API-Key": "wrong"})
    assert res.status_code == 403
    assert "error" in res.get_json()


@pytest.mark.auth
def test_post_with_correct_api_key_returns_201(client, auth_headers):
    res = client.post("/api/orders", json=SAMPLE, headers=auth_headers)
    assert res.status_code == 201


@pytest.mark.auth
def test_put_without_api_key_returns_401(client, auth_headers):
    order_id = client.post("/api/orders", json=SAMPLE, headers=auth_headers).get_json()[
        "id"
    ]
    res = client.put(f"/api/orders/{order_id}", json={"status": "fulfilled"})
    assert res.status_code == 401


@pytest.mark.auth
def test_put_with_wrong_api_key_returns_403(client, auth_headers):
    order_id = client.post("/api/orders", json=SAMPLE, headers=auth_headers).get_json()[
        "id"
    ]
    res = client.put(
        f"/api/orders/{order_id}",
        json={"status": "fulfilled"},
        headers={"X-API-Key": "bad"},
    )
    assert res.status_code == 403


@pytest.mark.auth
def test_put_with_correct_api_key_returns_200(client, auth_headers):
    order_id = client.post("/api/orders", json=SAMPLE, headers=auth_headers).get_json()[
        "id"
    ]
    res = client.put(
        f"/api/orders/{order_id}", json={"status": "fulfilled"}, headers=auth_headers
    )
    assert res.status_code == 200


@pytest.mark.auth
def test_delete_without_api_key_returns_401(client, auth_headers):
    order_id = client.post("/api/orders", json=SAMPLE, headers=auth_headers).get_json()[
        "id"
    ]
    res = client.delete(f"/api/orders/{order_id}")
    assert res.status_code == 401


@pytest.mark.auth
def test_delete_with_wrong_api_key_returns_403(client, auth_headers):
    order_id = client.post("/api/orders", json=SAMPLE, headers=auth_headers).get_json()[
        "id"
    ]
    res = client.delete(f"/api/orders/{order_id}", headers={"X-API-Key": "nope"})
    assert res.status_code == 403


@pytest.mark.auth
def test_delete_with_correct_api_key_returns_200(client, auth_headers):
    order_id = client.post("/api/orders", json=SAMPLE, headers=auth_headers).get_json()[
        "id"
    ]
    res = client.delete(f"/api/orders/{order_id}", headers=auth_headers)
    assert res.status_code == 200


@pytest.mark.auth
def test_get_endpoints_do_not_require_api_key(client):
    """GET endpoints must be publicly accessible."""
    assert client.get("/api/orders").status_code == 200
    assert client.get("/api/orders/stats").status_code == 200
    assert client.get("/api/health").status_code == 200
