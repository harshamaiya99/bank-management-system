import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tests.web_selenium.utils.actions import smart_fill, smart_click, get_text

class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    URL = "/login"

    # Locators
    USERNAME_INPUT = (By.NAME, "username")
    PASSWORD_INPUT = (By.NAME, "password")
    LOGIN_BTN = (By.CSS_SELECTOR, "button[type='submit']")
    ERROR_MSG = (By.CSS_SELECTOR, "[data-testid='login-error']")

    @allure.step("Navigate to Login Page")
    def navigate_to_login(self):
        self.driver.get(self.URL)

    @allure.step("Enter Username and Password and click Login button")
    def login(self, username, password):
        smart_fill(self.driver, self.USERNAME_INPUT, username)
        smart_fill(self.driver, self.PASSWORD_INPUT, password)
        smart_click(self.driver, self.LOGIN_BTN)

    def get_error_message(self):
        return get_text(self.driver, self.ERROR_MSG)