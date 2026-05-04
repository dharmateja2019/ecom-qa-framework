import pytest
from utils.api_client import get
from utils.api_auth import post_auth
from utils.schema_validator import (
    validate_schema,
    PRODUCT_SCHEMA_STRICT,
    PRODUCTS_LIST_SCHEMA,
    AUTH_RESPONSE_SCHEMA,
)


@pytest.mark.smoke
def test_products_list_matches_contract():
    response = get("/products")
    assert response.status_code == 200

    result = validate_schema(response.json(), PRODUCTS_LIST_SCHEMA)
    assert result["valid"], f"Products list contract violation: {result['error']}"


@pytest.mark.smoke
def test_single_product_matches_contract():
    response = get("/products/1")
    assert response.status_code == 200

    result = validate_schema(response.json(), PRODUCT_SCHEMA_STRICT)
    assert result["valid"], f"Product contract violation: {result['error']}"


@pytest.mark.regression
def test_auth_response_matches_contract():
    payload = {"username": "emilys", "password": "emilyspass"}
    response = post_auth("/auth/login", payload)
    assert response.status_code == 200

    result = validate_schema(response.json(), AUTH_RESPONSE_SCHEMA)
    assert result["valid"], f"Auth response contract violation: {result['error']}"


@pytest.mark.regression
def test_contract_catches_missing_field():
    # Simulate a broken API response missing required field
    broken_response = {
        "id": 1,
        "title": "Test Product",
        # price is missing — breaking change
        "category": "electronics",
        "stock": 10,
        "rating": 4.5,
        "brand": "TestBrand",
    }

    result = validate_schema(broken_response, PRODUCT_SCHEMA_STRICT)
    assert result["valid"] is False, "Schema validator should catch missing price field"
    assert (
        "price" in result["error"]
    ), f"Error should mention price field, got: {result['error']}"


@pytest.mark.regression
def test_contract_catches_wrong_data_type():
    # Simulate price coming as string instead of number
    broken_response = {
        "id": 1,
        "title": "Test Product",
        "price": "99.99",  # string instead of number — breaking change
        "category": "electronics",
        "stock": 10,
        "rating": 4.5,
        "brand": "TestBrand",
    }

    result = validate_schema(broken_response, PRODUCT_SCHEMA_STRICT)
    assert (
        result["valid"] is False
    ), "Schema validator should catch wrong data type for price"
