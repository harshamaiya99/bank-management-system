import allure
from tests.web_selenium.pages.base_page import BasePage

class HomePage(BasePage):

    # Selectors
    SEARCH_INPUT = "#accountId"
    SEARCH_BTN = "button.btn-search"
    CREATE_BTN = "button.btn-create"
    ERROR_MSG = "#errorMessage"

    @allure.step("Click Create Account Button")
    def go_to_create_account(self):
        self.click(self.CREATE_BTN)

    @allure.step("Search for Account")
    def search_account(self, account_id):
        self.fill(self.SEARCH_INPUT, account_id)
        self.click(self.SEARCH_BTN)

    @allure.step("Wait for details to load")
    def wait_for_details_to_load(self):
        # 'find' automatically waits for visibility based on BasePage logic
        self.find(self.ERROR_MSG)

    def get_error_message(self):
        return self.get_text(self.ERROR_MSG)