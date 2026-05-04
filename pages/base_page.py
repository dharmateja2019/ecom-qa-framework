from playwright.sync_api import Page
from config import settings


class BasePage:
    def __init__(self, page: Page):
        self.page = page

    def navigate(self, path: str = ""):
        url = f"{settings.BASE_URL}/{path}"
        self.page.goto(url)

    def get_title(self) -> str:
        return self.page.title()

    def get_url(self) -> str:
        return self.page.url
