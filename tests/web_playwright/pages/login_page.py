import allure
from tests.web_playwright.pages.base_page import BasePage


class LoginPage(BasePage):
    URL = "/login"

    # Locators
    # Using 'name' attribute is standard for React Hook Form + Shadcn
    USERNAME_INPUT = "input[name='username']"
    PASSWORD_INPUT = "input[name='password']"
    LOGIN_BTN = "button[type='submit']"
    # Shadcn form error message usually has this class
    ERROR_MSG = "p.text-destructive, div.text-destructive"

    @allure.step("Navigate to Login Page")
    def navigate_to_login(self):
        self.navigate(self.URL)

    @allure.step("Enter Username and Password and click Login button")
    def login(self, username, password):
        self.fill(self.USERNAME_INPUT, username)
        self.fill(self.PASSWORD_INPUT, password)
        self.click(self.LOGIN_BTN)

    def get_error_message(self):
        # Wait for the error message to appear in the DOM
        self.page.wait_for_selector(self.ERROR_MSG)
        return self.get_text(self.ERROR_MSG)