import pytest
from fastapi.testclient import TestClient

import database
from main import app


@pytest.fixture
def client(tmp_path):
    db_path = tmp_path / "test.db"

    database.set_db_name(str(db_path))
    database.init_db()

    with TestClient(app) as client:
        yield client


def test_root(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"message": "Item API is running"}


def test_create_item(client):
    response = client.post(
        "/items",
        json={
            "name": "pytest item",
            "category": "test",
            "price": 25,
            "quantity": 10,
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["id"] > 0
    assert data["name"] == "pytest item"
    assert data["category"] == "test"
    assert data["price"] == 25
    assert data["quantity"] == 10


def test_get_items(client):
    response = client.get("/items")

    assert response.status_code == 200
    assert response.json() == []


def test_get_item(client):
    create_response = client.post(
        "/items",
        json={
            "name": "test item",
            "category": "test",
            "price": 2,
            "quantity": 47,
        },
    )

    assert create_response.status_code == 201

    item_id = create_response.json()["id"]

    response = client.get(f"/items/{item_id}")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == item_id
    assert data["name"] == "test item"
    assert data["category"] == "test"
    assert data["price"] == 2
    assert data["quantity"] == 47


def test_update_item(client):
    # 建立資料
    create_response = client.post(
        "/items",
        json={
            "name": "test item",
            "category": "test",
            "price": 2,
            "quantity": 47,
        },
    )

    assert create_response.status_code == 201

    item_id = create_response.json()["id"]

    # 更新資料
    update_response = client.put(
        f"/items/{item_id}",
        json={
            "name": "test update",
            "category": "test",
            "price": 5,
            "quantity": 97,
        },
    )

    assert update_response.status_code == 200

    data = update_response.json()

    assert data["id"] == item_id
    assert data["name"] == "test update"
    assert data["category"] == "test"
    assert data["price"] == 5
    assert data["quantity"] == 97


def test_delete_item(client):
    # 建立資料
    create_response = client.post(
        "/items",
        json={
            "name": "test item",
            "category": "test",
            "price": 2,
            "quantity": 47,
        },
    )

    assert create_response.status_code == 201

    item_id = create_response.json()["id"]

    # 刪除資料
    delete_response = client.delete(
        f"/items/{item_id}",
    )

    assert delete_response.status_code == 204

    # 確認 get 拿不到資料
    get_response = client.get(f"/items/{item_id}")

    assert get_response.status_code == 404


@pytest.mark.parametrize("quantity", [0, 10000])
def test_create_item_valid_quantity(client, quantity):
    response = client.post(
        "/items",
        json={
            "name": "test item",
            "category": "test",
            "price": 2,
            "quantity": quantity,
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["name"] == "test item"
    assert data["category"] == "test"
    assert data["price"] == 2
    assert data["quantity"] == quantity
    assert data["id"] > 0


def test_create_item_invalid_type(client):
    response = client.post(
        "/items",
        json={
            "name": "invalid item",
            "category": "test",
            "price": 2,
            "quantity": "invalid",
        },
    )

    assert response.status_code == 422


@pytest.mark.parametrize("quantity", [-1, -10, -100])
def test_create_item_invalid_quantity(client, quantity):
    response = client.post(
        "/items",
        json={
            "name": "test item",
            "category": "test",
            "price": 2,
            "quantity": quantity,
        },
    )

    assert response.status_code == 422


def test_create_item_invalid_name(client):
    response = client.post(
        "/items",
        json={"name": "", "category": "test", "price": 2, "quantity": 6},
    )

    assert response.status_code == 422


def test_get_invalid_item_id(client):
    response = client.get("/items/999999")

    assert response.status_code == 404


def test_delete_invalid_item_id(client):
    response = client.delete("/items/999999")

    assert response.status_code == 404


@pytest.mark.parametrize("price", [-1, -10, -100])
def test_create_invalid_item_does_not_create_data(client, price):
    response = client.post(
        "/items",
        json={
            "name": "invalid item",
            "category": "test",
            "price": price,
            "quantity": 47,
        },
    )

    assert response.status_code == 422

    response = client.get("/items")

    assert response.status_code == 200
    assert response.json() == []


def test_update_item_invalid_quantity(client):
    create_response = client.post(
        "/items",
        json={
            "name": "test item",
            "category": "test",
            "price": 2,
            "quantity": 7354,
        },
    )

    assert create_response.status_code == 201
    item_id = create_response.json()["id"]

    response = client.put(
        f"/items/{item_id}",
        json={
            "name": "test update",
            "category": "test",
            "price": 2,
            "quantity": 17354,
        },
    )

    assert response.status_code == 400
    assert response.json() == {"detail": "Quantity can not greater than 10000"}
