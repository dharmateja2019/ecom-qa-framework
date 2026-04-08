import pytest
from utils.api_client import *

@pytest.fixture(scope="session")
def product_catalogue():
  get_response = get("/products")
  assert get_response.status_code == 200, "Failed to fetch product catalogue"
  return get_response.json()
