import allure
from selenium.webdriver.common.by import By
from tests.web_selenium.pages.base_page import BasePage

class HomePage(BasePage):
    # Selectors (Tuples)
    SEARCH_INPUT = (By.ID, "accountId")
    SEARCH_BTN = (By.CSS_SELECTOR, "button.btn-search")
    CREATE_BTN = (By.CSS_SELECTOR, "button.btn-create")
    ERROR_MSG = (By.ID, "errorMessage")

    @allure.step("Click Create Account Button")
    def go_to_create_account(self):
        self.click(self.CREATE_BTN)

    @allure.step("Search for Account")
    def search_account(self, account_id):
        self.fill(self.SEARCH_INPUT, account_id)
        self.click(self.SEARCH_BTN)

    @allure.step("Wait for details to load")
    def wait_for_details_to_load(self):
        self.find(self.ERROR_MSG)

    def get_error_message(self):
        return self.get_text(self.ERROR_MSG)