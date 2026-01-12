from playwright.sync_api import Page, expect
from tests.web_playwright.utils.alert_handler import AlertHandler

class BasePage:
    def __init__(self, page: Page):
        self.page = page
        self.alert = AlertHandler(page)  # Centralized Alert Handler

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

    def get_validation_message(self, selector: str) -> str:
        """
        Returns the browser's native validation message (the tooltip text).
        Using .first is useful for radio groups where multiple inputs have the same name.
        """
        return self.page.locator(selector).first.evaluate("element => element.validationMessage")
