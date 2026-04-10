import pytest
from utils.api_client import *
from playwright.sync_api import Page
from pages.home_page import HomePage

@pytest.mark.smoke
def test_dummyjson_loads_successfully(page: Page): # type: ignore
  home_page = HomePage(page)
  home_page.navigate()
  assert home_page.get_title() == "DummyJSON - Free Fake REST API for Placeholder JSON Data", "Storefront did not load successfully"

@pytest.mark.smoke
def test_dummyjson_page_is_accessible(page: Page):
  home_page = HomePage(page)
  home_page.navigate()
  assert home_page.get_url() == "https://dummyjson.com/", "Storefront URL is not accessible"

@pytest.mark.regression
@pytest.mark.skip(reason="UI does not display product count reliably")
def test_api_and_ui_count_match(product_catalogue, page: Page):
  api_count = len(product_catalogue)
  home_page = HomePage(page)
  home_page.navigate()
  ui_count = home_page.get_product_count_from_ui()
  assert api_count == ui_count, f"API returned {api_count} products but UI shows {ui_count}"

@pytest.mark.regression
def test_products_item_visible_on_storefront(page: Page):
    home = HomePage(page)
    home.navigate()
    
    # Verify UI loaded
    assert home.is_loaded(), "DummyJSON did not load"
