from playwright.sync_api import expect
import pytest
from pages.home_page import HomePage


@pytest.mark.regression
def test_stable_page_load(page):
    home = HomePage(page)
    home.navigate()

    # This element loads after JS execution — tests auto-wait
    expect(page.locator(".resources-container")).to_be_visible()
    expect(page.locator(".logo-title")).to_contain_text("DummyJSON")
