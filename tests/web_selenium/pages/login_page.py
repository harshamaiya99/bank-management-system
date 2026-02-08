import allure
from selenium.webdriver.common.by import By
from tests.web_selenium.pages.base_page import BasePage

class LoginPage(BasePage):
    URL = "/login"

    # Locators
    USERNAME_INPUT = (By.NAME, "username")
    PASSWORD_INPUT = (By.NAME, "password")
    LOGIN_BTN = (By.CSS_SELECTOR, "button[type='submit']")
    ERROR_MSG = (By.CSS_SELECTOR, "[data-testid='login-error']")

    @allure.step("Navigate to Login Page")
    def navigate_to_login(self):
        self.navigate(self.URL)

    @allure.step("Enter Username and Password and click Login button")
    def login(self, username, password):
        self.fill(self.USERNAME_INPUT, username)
        self.fill(self.PASSWORD_INPUT, password)
        self.click(self.LOGIN_BTN)

    def get_error_message(self):
        """Waits for the error message to appear and returns its text."""
        return self.get_text(self.ERROR_MSG)