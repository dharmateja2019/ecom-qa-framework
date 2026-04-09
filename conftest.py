import pytest
from utils.api_client import *

def is_api_reachable():
    try:
        response = get("/products")
        return response.status_code == 200
    except Exception:
        return False

@pytest.fixture(scope="session", autouse=True)
def check_api_availability():
    if not is_api_reachable():
        pytest.skip("API not reachable in this environment")
        
@pytest.fixture(scope="session")
def product_catalogue():
  get_response = get("/products")
  assert get_response.status_code == 200, "Failed to fetch product catalogue"
  return get_response.json()
