import allure
from selenium.webdriver.common.by import By
from tests.web_selenium.pages.base_page import BasePage

class HomePage(BasePage):
    URL = "/dashboard"

    # Locators
    SEARCH_INPUT = (By.CSS_SELECTOR, "input[placeholder*='Account ID']")
    # Using XPath for text matching similar to Playwright's :has-text()
    SEARCH_BTN = (By.XPATH, "//button[contains(., 'Search Account')]")
    CREATE_BTN = (By.XPATH, "//button[contains(., 'Create Account')]")
    LOGOUT_BTN = (By.XPATH, "//button[contains(., 'Logout')]")
    ERROR_MSG = (By.CSS_SELECTOR, "[data-testid='search-error']")

    @allure.step("Click Create Account Button")
    def go_to_create_account(self):
        self.click(self.CREATE_BTN)

    @allure.step("Navigate to Dashboard Page")
    def navigate_to_dashboard(self):
        self.navigate(self.URL)

    @allure.step("Provide Search Input and Click on Search Button")
    def search_account(self, account_id):
        self.fill(self.SEARCH_INPUT, str(account_id))
        self.click(self.SEARCH_BTN)

    @allure.step("Click Logout Button")
    def logout(self):
        self.click(self.LOGOUT_BTN)

    def get_error_message(self):
        return self.get_text(self.ERROR_MSG)