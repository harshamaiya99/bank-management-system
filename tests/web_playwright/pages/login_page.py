import allure
from playwright.sync_api import Page, expect


class LoginPage:
    def __init__(self, page: Page):
        self.page = page
    URL = "/login"


    @allure.step("Navigate to Login Page")
    def navigate_to_login(self):
        self.page.goto(self.URL)

    @allure.step("Enter Username and Password and click Login button")
    def login(self, username, password):
        # Targets the input labeled "Username" & "Password"
        self.page.get_by_label("Username").fill(str(username)) 
        self.page.get_by_label("Password").fill(str(password))
        # Targets the button that explicitly says "Sign In"
        self.page.get_by_role("button", name="Sign In").click()

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