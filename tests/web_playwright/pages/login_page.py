import allure
from playwright.sync_api import Page, expect


class LoginPage:
    def __init__(self, page: Page):
        self.page = page
    URL = "/login"

    # Locators
    # Using 'name' attribute is standard for React Hook Form + Shadcn
    USERNAME_INPUT = "input[name='username']"
    PASSWORD_INPUT = "input[name='password']"
    LOGIN_BTN = "button[type='submit']"

    @allure.step("Navigate to Login Page")
    def navigate_to_login(self):
        self.page.goto(self.URL)

    @allure.step("Enter Username and Password and click Login button")
    def login(self, username, password):
        self.page.locator(self.USERNAME_INPUT).fill(str(username))
        self.page.locator(self.PASSWORD_INPUT).fill(str(password))
        self.page.locator(self.LOGIN_BTN).click()

    # Define the locator as a property
    @property
    def error_msg(self):
        return self.page.get_by_test_id("login-error")

    # Update the method to use the locator
    def get_error_message(self):
        """
        Waits for the error message to appear and returns its text.
        """
        # Locator.wait_for() defaults to state="visible"
        self.error_msg.wait_for()
        return self.error_msg.text_content()