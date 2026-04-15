from playwright.sync_api import expect
from pages.home_page import HomePage

def test_stable_products(page):
    home = HomePage(page)
    home.navigate()

    # Stable assertion
    expect(page.locator(".product")).to_have_count(0)