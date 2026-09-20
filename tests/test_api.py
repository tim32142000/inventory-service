import pytest
from fastapi.testclient import TestClient

import database
from main import app


@pytest.fixture
def client(test_db):
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


def test_get_list_items(client):
    response = client.get("/items")

    assert response.status_code == 200
    assert response.json() == []


def test_get_all_items_filtered_by_category(client):
    food_response = client.post(
        "/items",
        json={
            "name": "apple",
            "category": "food",
            "price": 30,
            "quantity": 10,
        },
    )
    tool_response = client.post(
        "/items",
        json={
            "name": "hammer",
            "category": "tool",
            "price": 500,
            "quantity": 3,
        },
    )

    assert food_response.status_code == 201
    assert tool_response.status_code == 201

    response = client.get(
        "/items",
        params={"category": "food"},
    )

    assert response.status_code == 200
    assert response.json() == [food_response.json()]


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


def test_create_item_invalid_business_quantity(client):
    response = client.post(
        "/items",
        json={
            "name": "test item",
            "category": "test",
            "price": 2,
            "quantity": 10001,
        },
    )

    assert response.status_code == 400
    assert response.json() == {"detail": "Quantity can not greater than 10000"}

    get_response = client.get("/items")

    assert get_response.status_code == 200
    assert get_response.json() == []


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
            "quantity": 7300,
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
            "quantity": 17300,
        },
    )

    assert response.status_code == 400
    assert response.json() == {"detail": "Quantity can not greater than 10000"}

    get_response = client.get(f"/items/{item_id}")

    assert get_response.status_code == 200
    assert get_response.json() == {
        "id": item_id,
        "name": "test item",
        "category": "test",
        "price": 2,
        "quantity": 7300,
    }


@pytest.mark.parametrize(
    ("order", "expected_prices"), [("asc", [100, 300, 500]), ("desc", [500, 300, 100])]
)
def test_get_items_sorted_by_price(client, order, expected_prices):
    items = [
        {
            "name": "expensive",
            "price": 500,
        },
        {
            "name": "cheap",
            "price": 100,
        },
        {
            "name": "medium",
            "price": 300,
        },
    ]

    for item in items:
        response = client.post(
            "/items",
            json={
                "name": item["name"],
                "category": "test",
                "price": item["price"],
                "quantity": 1,
            },
        )

    assert response.status_code == 201

    response = client.get(
        "/items",
        params={
            "sort_by": "price",
            "order": order,
        },
    )

    assert response.status_code == 200

    prices = [item["price"] for item in response.json()]

    assert prices == expected_prices


@pytest.mark.parametrize(
    "params",
    [
        {
            "sort_by": "name",
            "order": "asc",
        },
        {
            "sort_by": "price",
            "order": "unknown",
        },
    ],
    ids=[
        "invalid-sort-field",
        "invalid-order",
    ],
)
def test_get_items_rejects_invalid_sorting(client, params):
    response = client.get(
        "/items",
        params=params,
    )

    assert response.status_code == 422


def test_get_items_filtered_and_sorted(client):
    items = [
        {
            "name": "expensive food",
            "category": "food",
            "price": 500,
        },
        {
            "name": "cheap tool",
            "category": "tool",
            "price": 50,
        },
        {
            "name": "cheap food",
            "category": "food",
            "price": 100,
        },
    ]

    for item in items:
        response = client.post(
            "/items",
            json={
                "name": item["name"],
                "category": item["category"],
                "price": item["price"],
                "quantity": 1,
            },
        )

        assert response.status_code == 201

    response = client.get(
        "/items",
        params={
            "category": "food",
            "sort_by": "price",
            "order": "asc",
        },
    )

    assert response.status_code == 200

    names = [item["name"] for item in response.json()]

    assert names == ["cheap food", "expensive food"]


def test_adjust_stock_increases_quantity(client):
    create_response = client.post(
        "/items",
        json={
            "name": "apple",
            "category": "food",
            "price": 30,
            "quantity": 10,
        },
    )

    assert create_response.status_code == 201

    item_id = create_response.json()["id"]

    response = client.post(f"/items/{item_id}/stock-adjustments", json={"change": 5})

    assert response.status_code == 200
    assert response.json()["quantity"] == 15


def test_adjust_stock_rejects_zero_change(client):
    create_response = client.post(
        "/items",
        json={
            "name": "apple",
            "category": "food",
            "price": 30,
            "quantity": 10,
        },
    )

    assert create_response.status_code == 201

    item_id = create_response.json()["id"]

    response = client.post(f"/items/{item_id}/stock-adjustments", json={"change": 0})

    assert response.status_code == 422

    get_response = client.get(f"/items/{item_id}")

    assert get_response.status_code == 200
    assert get_response.json()["quantity"] == 10
