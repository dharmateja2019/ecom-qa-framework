
import pytest
import sys
sys.path.append(".")  # To import from utils folder

from utils.api_client import *
from config.settings import SLA_SECONDS

# Scenario 1 — Get all products and validate the catalogue is not empty
    # Business context: if this API returns empty, the entire product listing page on the website shows nothing. That's a P1 production bug.
    # What to assert: status is 200, response is a list, list has more than 0 items, every product has id, title, price, category.
    # Write this test yourself. Call it test_all_products_returns_valid_catalogue.
@pytest.mark.smoke
def test_all_products_returns_valid_catalogue(product_catalogue):
  get_response = product_catalogue  # Using fixture from conftest.py
  products = get_response['products']
  assert isinstance(products, list)
  assert len(products) > 0
  for product in products:
    assert "id" in product
    assert "title" in product
    assert "price" in product
    assert "category" in product

# Scenario 2 — Get a single product and validate its data structure
    # Business context: the product detail page pulls from GET /products/1. If price is missing or zero, the buy button shows ₹0. That's a billing bug.
    # What to assert: status 200, product has price, price is greater than 0, product has title that is not empty.
    # Call it test_single_product_has_valid_price_and_title.
@pytest.mark.smoke
@pytest.mark.parametrize("product_id", [1,2,3])  # Test multiple product IDs
def test_single_product_has_valid_price_and_title(product_id,get_product):
  product = get_product(product_id)
  print(f"Testing product ID {product['id']}: {product['title']}")
  assert product["id"] == product_id
  assert product["price"] > 0
  assert product["title"].strip() != ""

# Scenario 3 — Get a non-existent product
    # Business context: what happens when someone types a wrong product ID in the URL? The API should handle it gracefully.
    # Hit GET /products/99999. What do you expect? Check it first by opening that URL in your browser. Then write the assertion based on what you actually see.
    # Call it test_invalid_product_id_returns_expected_response.
@pytest.mark.regression
def test_invalid_product_id_returns_expected_response():
  # BUG: This API returns 200 with null instead of 404
    # A correct REST API should return 404 for missing resources
    # Asserting actual behaviour for now — raise bug ticket separately
  get_response = get("/products/99999")
  assert get_response.status_code == 404
  # # assert get_response.headers["Content-Type"] == "application/json; charset=utf-8"
  # body = get_response.text
  # assert body == "", f"Expected null body for invalid ID, got: {body}"
  error_response = get_response.json()
  assert "message" in error_response
  assert error_response["message"] == "Product with id '99999' not found"

# Scenario 4 — Response time is within acceptable limit
    # Business context: if the product API takes more than 2 seconds, the website feels broken. Performance is a business requirement, not optional.
    # Assert response.elapsed.total_seconds() < 2.
    # Call it test_products_api_responds_within_sla.
@pytest.mark.smoke
def test_products_api_responds_within_sla():
  response_time =  get("/products").elapsed.total_seconds()
  print(f"Response time: {response_time} seconds")
  assert response_time < SLA_SECONDS, f"Response time {response_time:.2f}s exceeds SLA of {SLA_SECONDS}s"


# Scenario 5 — Filter products by category
    # Business context: the category filter on the website calls GET /products/category/electronics. If it returns products from other categories, the filter is broken.
    # Assert every product in the response has category == "electronics".
    # Call it test_category_filter_returns_only_correct_category.
@pytest.mark.regression
@pytest.mark.parametrize("category", [
    "beauty",
    "groceries",
    "furniture",
    "fragrances",
    "smartphones",
])
def test_each_category_returns_correct_products(category):
    response = get(f"/products/category/{category}")
    assert response.status_code == 200
    products = response.json()["products"]
    assert len(products) > 0
    for product in products:
        assert product["category"].lower() == category.lower()