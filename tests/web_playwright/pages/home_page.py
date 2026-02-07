import allure
from tests.web_playwright.pages.base_page import BasePage


class HomePage(BasePage):

    # Locators
    # Targeting by placeholder is robust for the Search Input
    SEARCH_INPUT = "input[placeholder*='Account ID']"
    # Targeting buttons by their visible text
    SEARCH_BTN = "button:has-text('Search Account')"
    CREATE_BTN = "button:has-text('Create Account')"
    LOGOUT_BTN = "button:has-text('Logout')"
    # Dashboard error message styling
    ERROR_MSG = "p.text-destructive"



    @allure.step("Click Create Account Button")
    def go_to_create_account(self):
        self.click(self.CREATE_BTN)

    @allure.step("Provide Search Input and Click on Search Button")
    def search_account(self, account_id):
        self.fill(self.SEARCH_INPUT, account_id)
        self.click(self.SEARCH_BTN)

    @allure.step("Click Logout Button")
    def logout(self):
        self.click(self.LOGOUT_BTN)

    def get_error_message(self):
        self.page.wait_for_selector(self.ERROR_MSG)
        return self.get_text(self.ERROR_MSG)