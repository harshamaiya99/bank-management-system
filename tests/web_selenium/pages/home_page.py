import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tests.web_selenium.utils.actions import smart_fill, smart_click, get_text

class HomePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    URL = "/dashboard"

    # Locators
    SEARCH_INPUT = (By.CSS_SELECTOR, "input[placeholder*='Account ID']")
    SEARCH_BTN = (By.XPATH, "//button[contains(., 'Search Account')]")
    CREATE_BTN = (By.XPATH, "//button[contains(., 'Create Account')]")
    LOGOUT_BTN = (By.XPATH, "//button[contains(., 'Logout')]")
    ERROR_MSG = (By.CSS_SELECTOR, "[data-testid='search-error']")

    @allure.step("Click Create Account Button")
    def go_to_create_account(self):
        smart_click(self.driver, self.CREATE_BTN)

    @allure.step("Navigate to Dashboard Page")
    def navigate_to_dashboard(self):
        self.driver.get(self.URL)

    @allure.step("Provide Search Input and Click on Search Button")
    def search_account(self, account_id):
        smart_fill(self.driver, self.SEARCH_INPUT, str(account_id))
        smart_click(self.driver, self.SEARCH_BTN)

    @allure.step("Click Logout Button")
    def logout(self):
        smart_click(self.driver, self.LOGOUT_BTN)

    def get_error_message(self):
        return get_text(self.driver, self.ERROR_MSG)