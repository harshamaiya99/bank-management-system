import allure
from tests.web_selenium.pages.base_page import BasePage


class LoginPage(BasePage):
    URL = "/login.html"

    # Locators
    USERNAME_INPUT = "#username"
    PASSWORD_INPUT = "#password"
    LOGIN_BTN = "button.btn-login"
    ERROR_MSG = "#error"

    @allure.step("Navigate to Login Page")
    def navigate_to_login(self):
        self.navigate(self.URL)

    @allure.step("Enter Username and Password and click Login button")
    def login(self, username, password):
        self.fill(self.USERNAME_INPUT, username)
        self.fill(self.PASSWORD_INPUT, password)
        self.click(self.LOGIN_BTN)

    def get_error_message(self):
        return self.get_text(self.ERROR_MSG)