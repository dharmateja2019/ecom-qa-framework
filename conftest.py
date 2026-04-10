import pytest
from utils.api_client import *


@pytest.fixture(scope="session")
def product_catalogue():
  get_response = get("/products")
  assert get_response.status_code == 200, "Failed to fetch product catalogue"
  return get_response.json()["products"]

@pytest.fixture(scope="session")
def get_product():
    def _get_product(product_id):
        response = get(f"/products/{product_id}")
        assert response.status_code == 200
        return response.json()
    return _get_product