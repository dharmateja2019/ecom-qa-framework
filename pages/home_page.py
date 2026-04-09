from pages.base_page import BasePage
class HomePage(BasePage):
  # Locators — all in one place
    PRODUCT_COUNT_LABEL = ".list-item-subheader"
    PRODUCT_ITEMS = ".MuiGrid-item"
    
    def get_product_count_from_ui(self):
        text = self.page.locator(self.PRODUCT_COUNT_LABEL).first.text_content()
        return int(text.split()[0]) # type: ignore # ignore type hinting for simplicity
    
    def get_visible_product_cards(self):
        return self.page.locator(self.PRODUCT_ITEMS).count()
    
    def is_loaded(self):
        return self.page.locator(self.PRODUCT_COUNT_LABEL).first.is_visible()
  