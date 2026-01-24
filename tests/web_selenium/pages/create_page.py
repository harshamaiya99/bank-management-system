import allure
import re
from selenium.webdriver.common.by import By
from tests.web_selenium.pages.base_page import BasePage


class CreatePage(BasePage):
    # --- Locators (Tuples) ---
    HEADER = (By.TAG_NAME, "h1")
    NAME_INPUT = (By.ID, "accountHolderName")
    DOB_INPUT = (By.ID, "dob")
    EMAIL_INPUT = (By.ID, "email")
    PHONE_INPUT = (By.ID, "phone")
    ADDRESS_INPUT = (By.ID, "address")
    ZIP_INPUT = (By.ID, "zipCode")
    TYPE_SELECT = (By.ID, "accountType")
    BALANCE_INPUT = (By.ID, "balance")
    MARKETING_CHK = (By.ID, "marketingOptIn")
    TERMS_CHK = (By.ID, "agreedToTerms")
    SUBMIT_BTN = (By.CSS_SELECTOR, "button[type='submit']")

    @allure.step("Enter account holder name")
    def enter_name(self, name):
        self.fill(self.NAME_INPUT, name)

    @allure.step("Enter date of birth")
    def enter_dob(self, dob):
        self.set_value_js(self.DOB_INPUT, dob)

    @allure.step("Select gender")
    def select_gender(self, gender):
        # Dynamic Tuple construction
        locator = (By.CSS_SELECTOR, f"input[name='gender'][value='{gender}']")
        self.click(locator)

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
        self.select_option(self.TYPE_SELECT, account_type)

    @allure.step("Enter initial balance")
    def enter_balance(self, balance):
        self.fill(self.BALANCE_INPUT, balance)

    @allure.step("Select services")
    def select_services(self, services):
        if services:
            for service in services.split(","):
                # Dynamic Tuple for checkboxes
                locator = (By.CSS_SELECTOR, f"input[name='services'][value='{service.strip()}']")
                self.check(locator)

    @allure.step("Set marketing opt-in")
    def set_marketing_opt_in(self, opt_in):
        if opt_in == "true":
            self.check(self.MARKETING_CHK)

    @allure.step("Accept terms and conditions")
    def accept_terms(self):
        self.check(self.TERMS_CHK)

    @allure.step("Submit create account form")
    def submit_form_and_capture_account_id(self) -> tuple[str, str]:
        self.click(self.SUBMIT_BTN)

        alert_text = self.get_alert_text() or ""

        account_id = None
        match = re.search(r"ID:\s*(\d+)", alert_text)
        if match:
            account_id = match.group(1)

        # Wait for redirect to home (root path)
        self.wait_for_url("/")

        return account_id, alert_text

    def create_new_account(self, data: dict) -> tuple[str, str]:
        # --- SYNC FIX: Wait for specific text to ensure page transition ---
        self.wait_for_text(self.HEADER, "Open New Bank Account")
        # ------------------------------------

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