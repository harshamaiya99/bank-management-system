import allure
from tests.web_playwright.pages.base_page import BasePage


class HomePage(BasePage):
    URL = "/"

    # Locators
    SEARCH_INPUT = "#accountId"
    SEARCH_BTN = "button.btn-search"
    CREATE_BTN = "button.btn-create"
    ERROR_MSG = "#errorMessage"

    @allure.step("Navigate to Home Page")
    def navigate_to_home(self):
        self.navigate(self.URL)

    @allure.step("Click Create Account Button")
    def go_to_create_account(self):
        self.click(self.CREATE_BTN)

    @allure.step("Provide Search Input and Click on Search Button")
    def search_account(self, account_id):
        self.fill(self.SEARCH_INPUT, account_id)
        self.click(self.SEARCH_BTN)

    def get_error_message(self):
        self.page.wait_for_selector(self.ERROR_MSG)
        return self.get_text(self.ERROR_MSG)