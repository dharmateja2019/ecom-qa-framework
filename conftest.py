from urllib import response

import pytest
from utils.api_client import *


@pytest.fixture(scope="session")
def product_catalogue():
  def _get_product_catalogue(payload=None):
    response = get("/products", params=payload)
    assert response.status_code == 200, "Failed to fetch product catalogue"
    return response.json()
  return _get_product_catalogue

@pytest.fixture(scope="session")
def get_product():
    def _get_product(product_id):
        response = get(f"/products/{product_id}")
        assert response.status_code == 200
        return response.json()
    return _get_product

@pytest.fixture(scope="session")
def get_category_products():
   def _get_category_products(category_name):
      response = get(f"/products/category/{category_name}")
      assert response.status_code == 200
      return response.json()["products"]
   return _get_category_products

@pytest.fixture(scope="session")
def auth_token():
  payload = {
        "username": "emilys",
        "password": "emilyspass"
    }
  response = post("/auth/login", payload)
  assert response.status_code == 200, "Authentication failed"
  token = response.json()["accessToken"]
  assert token is not None, "No token returned"
  return token
