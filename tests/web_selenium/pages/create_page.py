import allure
import re
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tests.web_selenium.pages.base_page import BasePage


class CreatePage(BasePage):
    # Standard Inputs
    NAME_INPUT = (By.NAME, "account_holder_name")
    DOB_INPUT = (By.NAME, "dob")
    EMAIL_INPUT = (By.NAME, "email")
    PHONE_INPUT = (By.NAME, "phone")
    ADDRESS_INPUT = (By.NAME, "address")
    ZIP_INPUT = (By.NAME, "zip_code")
    BALANCE_INPUT = (By.NAME, "balance")
    SUBMIT_BTN = (By.CSS_SELECTOR, "button[type='submit']")

    TOAST_TITLE = (By.CSS_SELECTOR, "ol li .grid > div:nth-child(1)")
    TOAST_DESC = (By.CSS_SELECTOR, "ol li .grid > div:nth-child(2)")

    @allure.step("Enter account holder name")
    def enter_name(self, name):
        self.fill(self.NAME_INPUT, name)

    @allure.step("Enter date of birth")
    def enter_dob(self, dob):
        self.fill(self.DOB_INPUT, dob)

    @allure.step("Select gender")
    def select_gender(self, gender):
        self.click((By.CSS_SELECTOR, f"button[role='radio'][value='{gender}']"))

    @allure.step("Enter email")
    def enter_email(self, email):
        self.fill(self.EMAIL_INPUT, email)

    @allure.step("Enter phone number")
    def enter_phone(self, phone):
        self.fill(self.PHONE_INPUT, phone)

    @allure.step("Enter address")
    def enter_address(self, address):
        self.fill(self.ADDRESS_INPUT, address)

    @allure.step("Enter zip code")
    def enter_zip(self, zip_code):
        self.fill(self.ZIP_INPUT, zip_code)

    @allure.step("Select account type")
    def select_account_type(self, account_type):
        # Trigger
        trigger = (By.XPATH, "//label[contains(., 'Account Type')]/following::button[@role='combobox'][1]")
        self.click(trigger)
        # Option
        option = (By.XPATH, f"//div[@role='option']//span[contains(text(), '{account_type}')]")
        # Explicit wait for animation
        self.wait.until(EC.visibility_of_element_located(option))
        self.click(option)

    @allure.step("Enter initial balance")
    def enter_balance(self, balance):
        self.fill(self.BALANCE_INPUT, balance)

    @allure.step("Select services")
    def select_services(self, services):
        if services:
            for service in services.split(","):
                text = service.strip()
                # 1. Find Label to get the ID (robust against nested divs)
                label_el = self.find((By.XPATH, f"//label[contains(., '{text}')]"))
                target_id = label_el.get_attribute("for")

                # 2. Determine Locator
                if target_id:
                    locator = (By.ID, target_id)
                else:
                    # Fallback if no 'for' attribute
                    locator = (By.XPATH, f"//label[contains(., '{text}')]//button[@role='checkbox']")

                # 3. Check
                self.check(locator)

    @allure.step("Set marketing opt-in")
    def set_marketing_opt_in(self, opt_in):
        text = "Marketing Communications"
        # 1. Find Label
        label_el = self.find((By.XPATH, f"//label[contains(., '{text}')]"))
        target_id = label_el.get_attribute("for")

        # 2. Determine Locator
        if target_id:
            locator = (By.ID, target_id)
        else:
            locator = (By.XPATH, f"//label[contains(., '{text}')]//button[@role='checkbox']")

        # 3. Set State
        if str(opt_in).lower() == "true":
            self.check(locator)
        else:
            self.uncheck(locator)

    @allure.step("Accept terms and conditions")
    def accept_terms(self):
        text = "Terms and Conditions"
        # 1. Find Label
        label_el = self.find((By.XPATH, f"//label[contains(., '{text}')]"))
        target_id = label_el.get_attribute("for")

        # 2. Determine Locator
        if target_id:
            locator = (By.ID, target_id)
        else:
            locator = (By.XPATH, f"//label[contains(., '{text}')]//button[@role='checkbox']")

        # 3. Check
        self.check(locator)

    @allure.step("Submit create account form")
    def submit_form_and_capture_account_id(self) -> tuple[str, str, str]:
        self.click(self.SUBMIT_BTN)

        toast_text = self.get_text(self.TOAST_TITLE)
        toast_desc = self.get_text(self.TOAST_DESC)

        # Longer wait for backend processing (15s) to avoid TimeoutException
        WebDriverWait(self.driver, 15).until(EC.url_contains("/account-details/"))

        current_url = self.driver.current_url
        match = re.search(r"/account-details/(\d+)", current_url)
        account_id = match.group(1) if match else None

        return account_id, toast_text, toast_desc

    def create_new_account(self, data: dict) -> tuple[str, str, str]:
        self.enter_name(data["account_holder_name"])
        self.enter_dob(data["dob"])
        self.select_gender(data["gender"])
        self.enter_email(data["email"])
        self.enter_phone(data["phone"])
        self.enter_address(data["address"])
        self.enter_zip(data["zip_code"])
        self.select_account_type(data["account_type"])
        self.enter_balance(data["balance"])
        self.select_services(data["services"])
        self.set_marketing_opt_in(data["marketing_opt_in"])
        self.accept_terms()
        return self.submit_form_and_capture_account_id()