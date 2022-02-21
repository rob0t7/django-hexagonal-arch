import dataclasses
from typing import Any
from uuid import UUID

import pytest
from rest_framework.response import Response
from rest_framework.test import APIClient


def is_uuid_valid(uuid_str: str) -> bool:
    try:
        UUID(uuid_str)
        return True
    except ValueError:
        return False


PRODUCTS_PATH = "/products/"
CARTS_PATH = "/cart/"


@dataclasses.dataclass
class ProductData:
    name: str
    price: str
    sku: str

    def to_dict(self) -> dict[str, Any]:
        return {"name": self.name, "price": self.price, "sku": self.sku}


@pytest.fixture
def api_client() -> APIClient:
    return APIClient()


@pytest.fixture
def product_data() -> ProductData:
    return ProductData(name="Bananas", price="10.99", sku="BAN")


def create_product(api_client: APIClient, product: ProductData) -> Response:
    request_data = product.to_dict()
    return api_client.post(PRODUCTS_PATH, request_data, format="json")


def verify_product_response_body(data: dict[str, Any], product: ProductData) -> None:
    assert is_uuid_valid(data["id"])
    assert data["name"] == product.name
    assert data["price"] == product.price
    assert data["sku"] == product.sku


@pytest.mark.django_db
def test_create_product(api_client: APIClient, product_data: ProductData) -> None:
    response = create_product(api_client, product_data)
    assert response.status_code == 201
    verify_product_response_body(response.data, product_data)


@pytest.mark.django_db
def test_retrieve_all_products(
    api_client: APIClient, product_data: ProductData
) -> None:
    response = api_client.get(PRODUCTS_PATH)
    assert response.status_code == 200
    assert len(response.data) == 0

    assert create_product(api_client, product_data).status_code == 201

    response = api_client.get(PRODUCTS_PATH)
    assert response.status_code == 200
    assert len(response.data) == 1
    verify_product_response_body(response.data[0], product_data)


@pytest.mark.django_db
def test_create_cart(api_client: APIClient) -> None:
    response = api_client.post(CARTS_PATH, {}, format="json")
    assert response.status_code == 201
    assert is_uuid_valid(response.data["id"])
    assert len(response.data["items"]) == 0


@pytest.fixture
def product(api_client: APIClient, product_data: ProductData) -> Any:
    response = create_product(api_client, product_data)
    assert response.status_code == 201
    return response.data


def verify_cart_item(
    resp_body: dict[str, Any], product: ProductData, quantity: int = 1
) -> None:
    assert is_uuid_valid(resp_body["id"])
    assert resp_body["product_name"] == product.name
    assert resp_body["price"] == product.price
    assert resp_body["quantity"] == quantity


@pytest.mark.django_db
def test_add_item_to_cart(
    api_client: APIClient, product: Any, product_data: ProductData
) -> None:
    response = api_client.post(CARTS_PATH, {}, format="json")
    assert response.status_code == 201
    cart_id = response.data["id"]

    response = api_client.post(
        f"{CARTS_PATH}{cart_id}/items/",
        {"product_id": product["id"]},
        format="json",
    )
    assert response.status_code == 204

    response = api_client.get(f"{CARTS_PATH}{cart_id}/")
    assert response.status_code == 200
    assert len(response.data["items"]) == 1
    verify_cart_item(response.data["items"][0], product_data)


@pytest.mark.django_db
def test_add_product_twice_to_cart(
    api_client: APIClient, product: Any, product_data: ProductData
) -> None:
    response = api_client.post(CARTS_PATH, {}, format="json")
    assert response.status_code == 201
    cart_id = response.data["id"]

    for i in range(0, 2):
        response = api_client.post(
            f"{CARTS_PATH}{cart_id}/items/",
            {"product_id": product["id"]},
            format="json",
        )
        assert response.status_code == 204

    response = api_client.get(f"{CARTS_PATH}{cart_id}/")
    assert response.status_code == 200
    assert len(response.data["items"]) == 1
    verify_cart_item(response.data["items"][0], product_data, 2)


@pytest.mark.django_db
def test_update_quantity_on_cart_item(
    api_client: APIClient, product: Any, product_data: ProductData
) -> None:
    response = api_client.post(CARTS_PATH, {}, format="json")
    assert response.status_code == 201
    cart_id = response.data["id"]

    response = api_client.post(
        f"{CARTS_PATH}{cart_id}/items/",
        {"product_id": product["id"]},
        format="json",
    )
    assert response.status_code == 204

    response = api_client.get(f"{CARTS_PATH}{cart_id}/")
    assert response.status_code == 200
    assert len(response.data["items"]) == 1
    verify_cart_item(response.data["items"][0], product_data)

    cart_item_id = response.data["items"][0]["id"]

    response = api_client.patch(
        f"{CARTS_PATH}{cart_id}/items/{cart_item_id}/",
        {"quantity": 10},
        format="json",
    )
    assert response.status_code == 204


# @pytest.mark.django_db
# def test_updating_quantity_from_item(api_client: APIClient, product: Any) -> None:
#      response = api_client.post(CARTS_PATH, {}, format="json")
#     assert response.status_code == 201
#     cart_id = response.data["id"]

#     for i in range(0, 2):
#         response = api_client.post(
#             f"{CARTS_PATH}{cart_id}/items/",
#             {"product_id": product["id"]},
#             format="json",
#         )
#         assert response.status_code == 204
#     response = api_client.get(f"{CARTS_PATH}{cart_id}/")
#     assert response.status_code == 200
#     assert len(response.data["items"]) == 1
#     assert response.data["items"][0] == {
#         "price": product["price"],
#         "product_id": product["id"],
#         "quantity": 2,
#         "product_name": product["name"],
#     }
