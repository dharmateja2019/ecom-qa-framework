import pytest
from utils.api_client import *
from playwright.sync_api import Page
from pages.home_page import HomePage

@pytest.mark.smoke
def test_storefront_loads_successfully(page: Page): # type: ignore
  home_page = HomePage(page)
  home_page.navigate()
  assert home_page.get_title() == "Fake Store API", "Storefront did not load successfully"

@pytest.mark.smoke
def test_storefront_page_is_accessible(page: Page):
  home_page = HomePage(page)
  home_page.navigate()
  assert home_page.get_url() == "https://fakestoreapi.com/", "Storefront URL is not accessible"

@pytest.mark.regression
def test_api_and_ui_count_match(product_catalogue, page: Page):
  api_count = len(product_catalogue)
  home_page = HomePage(page)
  home_page.navigate()
  ui_count = home_page.get_product_count_from_ui()
  assert api_count == ui_count, f"API returned {api_count} products but UI shows {ui_count}"