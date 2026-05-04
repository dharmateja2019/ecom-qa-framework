import pytest
from playwright.sync_api import expect, Page

from pages.home_page import HomePage


@pytest.mark.smoke
def test_dummyjson_loads_successfully(page: Page):
    home = HomePage(page)
    home.navigate()

    assert (
        home.get_title()
        == "DummyJSON - Free Fake REST API for Placeholder JSON Data"
    ), "Storefront did not load successfully"


@pytest.mark.smoke
def test_dummyjson_page_is_accessible(page: Page):
    home = HomePage(page)
    home.navigate()

    assert home.get_url() == "https://dummyjson.com/"


@pytest.mark.regression
def test_stable_page_load(page: Page):
    home = HomePage(page)
    home.navigate()

    expect(page.locator(".resources-container")).to_be_visible()
    expect(page.locator(".logo-title")).to_contain_text("DummyJSON")


@pytest.mark.regression
def test_products_item_visible_on_storefront(page: Page):
    home = HomePage(page)
    home.navigate()

    assert home.is_loaded()
