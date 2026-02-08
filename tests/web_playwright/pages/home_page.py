import allure
from playwright.sync_api import Page, expect


class HomePage:
    def __init__(self, page: Page):
        self.page = page

    URL = "/dashboard"

    # Locators
    # Targeting by placeholder is robust for the Search Input
    SEARCH_INPUT = "input[placeholder*='Account ID']"
    # Targeting buttons by their visible text
    SEARCH_BTN = "button:has-text('Search Account')"
    CREATE_BTN = "button:has-text('Create Account')"
    LOGOUT_BTN = "button:has-text('Logout')"

    @allure.step("Click Create Account Button")
    def go_to_create_account(self):
        self.page.locator(self.CREATE_BTN).click()

    @allure.step("Navigate to Dashboard Page")
    def navigate_to_dashboard(self):
        self.page.goto(self.URL)

    @allure.step("Provide Search Input and Click on Search Button")
    def search_account(self, account_id):
        self.page.locator(self.SEARCH_INPUT).fill(str(account_id))
        self.page.locator(self.SEARCH_BTN).click()

    @allure.step("Click Logout Button")
    def logout(self):
        self.page.locator(self.LOGOUT_BTN).click()

    # Define the locator as a property
    @property
    def error_msg(self):
        return self.page.get_by_test_id("search-error")

    # Update the method to use the locator
    def get_error_message(self):
        """
        Waits for the error message to appear and returns its text.
        """
        # Locator.wait_for() defaults to state="visible"
        self.error_msg.wait_for()
        return self.error_msg.text_content()