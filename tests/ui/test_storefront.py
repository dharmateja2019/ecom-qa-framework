import pytest
from utils.api_client import *
from playwright.sync_api import Page

@pytest.mark.smoke
def test_storefront_loads_successfully(page: Page):
  page.goto("https://fakestoreapi.com")
  assert page.title() == "Fake Store API", "Storefront did not load successfully"

@pytest.mark.smoke
def test_storefront_page_is_accessible(page: Page):
  page.goto("https://fakestoreapi.com")
  assert page.url == "https://fakestoreapi.com/", "Storefront URL is not accessible"

@pytest.mark.regression
def test_api_and_ui_count_match(product_catalogue, page: Page):
  api_count = len(product_catalogue)
  page.goto("https://fakestoreapi.com")
  ui_text = page.locator(".list-item-subheader").first.text_content()
  ui_count = int(ui_text.split()[0]) # type: ignore
  assert api_count == ui_count, f"API returned {api_count} products but UI shows {ui_count}"