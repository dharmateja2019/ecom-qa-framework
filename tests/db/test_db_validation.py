import pytest
from utils.api_client import get
from utils.db_helper import (
    insert_product,
    get_product_by_id,
    get_products_by_category,
)


@pytest.mark.regression
def test_api_product_matches_db_record():
    # Get product from API
    response = get("/products/1")
    api_product = response.json()

    # Simulate saving to DB (in real system, API call triggers DB write)
    insert_product(
        api_product["id"],
        api_product["title"],
        api_product["price"],
        api_product["category"],
    )

    # Validate DB record matches API response
    db_record = get_product_by_id(1)

    assert db_record is not None, "Product not found in DB"
    assert db_record[0] == api_product["id"]
    assert db_record[1] == api_product["title"]
    assert db_record[2] == api_product["price"]
    assert db_record[3] == api_product["category"]


@pytest.mark.regression
def test_category_products_stored_correctly():
    response = get("/products/category/smartphones")
    api_products = response.json()["products"]

    # Store all in DB
    for p in api_products:
        insert_product(p["id"], p["title"], p["price"], p["category"])

    # Validate DB has correct count
    db_products = get_products_by_category("smartphones")
    assert len(db_products) == len(
        api_products
    ), f"API has {len(api_products)} smartphones but DB has {len(db_products)}"


@pytest.mark.regression
def test_db_rejects_duplicate_handling():
    # Insert same product twice
    insert_product(999, "Test Product", 9.99, "test")
    insert_product(999, "Updated Product", 19.99, "test")

    # Should have latest version only
    db_record = get_product_by_id(999)
    assert db_record[1] == "Updated Product"
    assert db_record[2] == 19.99
