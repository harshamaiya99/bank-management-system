from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def navigate(self, url):
        self.driver.get(url)

    def find(self, locator):
        """
        Locates a single element.
        Args:
            locator: A tuple like (By.ID, "someId") or (By.CSS_SELECTOR, ".class")
        """
        return self.wait.until(EC.visibility_of_element_located(locator))

    def find_all(self, locator):
        """
        Locates all matching elements.
        Args:
            locator: A tuple like (By.CSS_SELECTOR, ".someClass")
        """
        return self.driver.find_elements(*locator)

    def click(self, locator):
        # Wait for element to be clickable before clicking
        element = self.wait.until(EC.element_to_be_clickable(locator))
        element.click()

    def fill(self, locator, text):
        element = self.find(locator)
        element.clear()
        element.send_keys(str(text))

    def select_option(self, locator, text):
        element = self.find(locator)
        select = Select(element)
        select.select_by_visible_text(text)

    def check(self, locator):
        """Ensures a checkbox/radio is checked"""
        element = self.find(locator)
        if not element.is_selected():
            element.click()

    def uncheck(self, locator):
        """Ensures a checkbox is unchecked"""
        element = self.find(locator)
        if element.is_selected():
            element.click()

    def get_text(self, locator):
        return self.find(locator).text

    def get_input_value(self, locator):
        return self.find(locator).get_attribute("value")

    def is_checked(self, locator):
        return self.find(locator).is_selected()

    def wait_for_url(self, partial_url):
        self.wait.until(EC.url_contains(partial_url))

    def set_value_js(self, locator, value):
        """
        Sets value using JavaScript (Crucial for your date inputs).
        """
        element = self.find(locator)
        self.driver.execute_script("arguments[0].value = arguments[1];", element, str(value))

    # def get_validation_message(self, locator):
    #     element = self.find(locator)
    #     return element.get_property("validationMessage")

    def get_alert_text(self):
        """
        Waits for alert, gets text, accepts it. Returns None if no alert.
        """
        try:
            alert = self.wait.until(EC.alert_is_present())
            text = alert.text
            alert.accept()
            return text
        except:
            return None