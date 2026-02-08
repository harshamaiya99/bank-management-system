import sys
import allure
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def navigate(self, url):
        self.driver.get(url)

    def find(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))

    def find_all(self, locator):
        return self.driver.find_elements(*locator)

    def _perform_robust_click(self, element):
        """
        Helper to handle ElementClickInterceptedException (e.g., toast messages).
        1. Try standard click.
        2. If intercepted, scroll to center and retry.
        3. If still intercepted, force click via JS.
        """
        try:
            element.click()
        except ElementClickInterceptedException:
            # Scroll element to center to avoid sticky headers/footers/toasts
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
            try:
                element.click()
            except ElementClickInterceptedException:
                # Force click if still covered
                self.driver.execute_script("arguments[0].click();", element)

    def click(self, locator):
        element = self.wait.until(EC.element_to_be_clickable(locator))
        self._perform_robust_click(element)

    def fill(self, locator, text):
        """
        Robust fill method that handles React controlled inputs.
        """
        element = self.find(locator)
        # Ensure we can focus the element even if partially covered
        self._perform_robust_click(element)

        # 1. Try standard clear
        element.clear()

        # 2. Check if clear worked (common failure in React/Shadcn)
        if element.get_attribute("value"):
            # Determine OS for correct modifier key
            cmd_ctrl = Keys.COMMAND if sys.platform == 'darwin' else Keys.CONTROL

            # Select All -> Backspace
            element.send_keys(cmd_ctrl + "a")
            element.send_keys(Keys.BACKSPACE)

        # 3. Type new text
        element.send_keys(str(text))

    def get_text(self, locator):
        return self.find(locator).text

    def get_input_value(self, locator):
        return self.find(locator).get_attribute("value")

    def is_checked(self, locator):
        return self.find(locator).is_selected()

    def wait_for_url(self, partial_url):
        self.wait.until(EC.url_contains(partial_url))

    def check(self, locator):
        element = self.find(locator)

        # 1. Handle ARIA Checkbox (Shadcn/Radix UI)
        if element.get_attribute("role") == "checkbox":
            if element.get_attribute("aria-checked") != "true":
                self._perform_robust_click(element)

        # 2. Handle Standard <input type="checkbox">
        else:
            if not element.is_selected():
                self._perform_robust_click(element)

    def uncheck(self, locator):
        element = self.find(locator)

        # 1. Handle ARIA Checkbox
        if element.get_attribute("role") == "checkbox":
            if element.get_attribute("aria-checked") == "true":
                self._perform_robust_click(element)

        # 2. Handle Standard <input>
        else:
            if element.is_selected():
                self._perform_robust_click(element)
