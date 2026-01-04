from playwright.sync_api import Page, expect

class BasePage:
    def __init__(self, page: Page):
        self.page = page

    def navigate(self, url: str):
        self.page.goto(url)

    def click(self, selector: str):
        self.page.locator(selector).click()

    def fill(self, selector: str, text: str):
        self.page.locator(selector).fill(str(text))

    def select_option(self, selector: str, value: str):
        self.page.locator(selector).select_option(value)

    def check(self, selector: str):
        self.page.locator(selector).check()

    def get_text(self, selector: str) -> str:
        return self.page.locator(selector).text_content()

    def get_input_value(self, selector: str) -> str:
        return self.page.locator(selector).input_value()

    def is_visible(self, selector: str) -> bool:
        return self.page.locator(selector).is_visible()
