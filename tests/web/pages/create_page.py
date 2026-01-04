import allure
import re
from tests.web.pages.base_page import BasePage


class CreatePage(BasePage):
    NAME_INPUT = "#accountHolderName"
    DOB_INPUT = "#dob"
    EMAIL_INPUT = "#email"
    PHONE_INPUT = "#phone"
    ADDRESS_INPUT = "#address"
    ZIP_INPUT = "#zipCode"
    TYPE_SELECT = "#accountType"
    BALANCE_INPUT = "#balance"
    MARKETING_CHK = "#marketingOptIn"
    TERMS_CHK = "#agreedToTerms"
    SUBMIT_BTN = "button[type='submit']"

    @allure.step("Enter account holder name]")
    def enter_name(self, name):
        self.fill(self.NAME_INPUT, name)

    @allure.step("Enter date of birth")
    def enter_dob(self, dob):
        self.fill(self.DOB_INPUT, dob)

    @allure.step("Select gender")
    def select_gender(self, gender):
        self.click(f"input[name='gender'][value='{gender}']")

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
                self.check(f"input[name='services'][value='{service.strip()}']")

    @allure.step("Set marketing opt-in")
    def set_marketing_opt_in(self, opt_in):
        if opt_in == "True":
            self.check(self.MARKETING_CHK)

    @allure.step("Accept terms and conditions")
    def accept_terms(self):
        self.check(self.TERMS_CHK)

    @allure.step("Submit create account form")
    def submit_form_and_capture_account_id(self) -> str:
        account_id = None

        def handle_dialog(dialog):
            nonlocal account_id
            match = re.search(r"ID:\s*(\d+)", dialog.message)
            if match:
                account_id = match.group(1)
            dialog.accept()

        self.page.once("dialog", handle_dialog)
        self.click(self.SUBMIT_BTN)
        self.page.wait_for_load_state("networkidle")
        return account_id

    def create_new_account(self, data: dict) -> str:
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
