import allure
import re
from tests.web_selenium.pages.base_page import BasePage # Changed Import

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class CreatePage(BasePage):
    NAME_INPUT = "#accountHolderName"
    DOB_INPUT = "#dob"
    GENDER_RADIO = "input[name='gender']"
    EMAIL_INPUT = "#email"
    PHONE_INPUT = "#phone"
    ADDRESS_INPUT = "#address"
    ZIP_INPUT = "#zipCode"
    TYPE_SELECT = "#accountType"
    BALANCE_INPUT = "#balance"
    MARKETING_CHK = "#marketingOptIn"
    SERVICE_SELECT = "input[name='services']"
    TERMS_CHK = "#agreedToTerms"
    SUBMIT_BTN = "button[type='submit']"

    @allure.step("Enter account holder name")
    def enter_name(self, name):
        self.fill(self.NAME_INPUT, name)

    @allure.step("Enter date of birth")
    def enter_dob(self, dob):
        # Use JS to bypass date input mask
        self.set_value_js(self.DOB_INPUT, dob)

    @allure.step("Select gender")
    def select_gender(self, gender):
        self.click(f"{self.GENDER_RADIO}[value='{gender}']")

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
                self.check(f"{self.SERVICE_SELECT}[value='{service.strip()}']")

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

        # alert()
        alert = WebDriverWait(self.driver, 5).until(EC.alert_is_present())
        alert_text = alert.text
        alert.accept()

        account_id = None
        match = re.search(r"ID:\s*(\d+)", alert_text)
        if match:
            account_id = match.group(1)

        self.wait_for_url("")

        return account_id, alert_text

    def create_new_account(self, data: dict) -> tuple[str, str]:
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

    def get_validation_message_for_field(self, field_name: str) -> str:
        locator_map = {
            "name": self.NAME_INPUT,
            "dob": self.DOB_INPUT,
            "gender": self.GENDER_RADIO,
            "email": self.EMAIL_INPUT,
            "phone": self.PHONE_INPUT,
            "address": self.ADDRESS_INPUT,
            "zip": self.ZIP_INPUT,
            "account_type": self.TYPE_SELECT,
            "balance": self.BALANCE_INPUT,
            "terms": self.TERMS_CHK
        }
        return self.get_validation_message(locator_map[field_name])