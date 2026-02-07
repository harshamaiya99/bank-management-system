import allure
import re
from tests.web_playwright.pages.base_page import BasePage


class CreatePage(BasePage):
    # Standard Inputs
    NAME_INPUT = "input[name='account_holder_name']"
    DOB_INPUT = "input[name='dob']"
    EMAIL_INPUT = "input[name='email']"
    PHONE_INPUT = "input[name='phone']"
    ADDRESS_INPUT = "input[name='address']"
    ZIP_INPUT = "input[name='zip_code']"
    BALANCE_INPUT = "input[name='balance']"

    SUBMIT_BTN = "button[type='submit']"

    # Toast Locator - CSS path is: ol (Viewport) -> li (Toast) -> div (Grid) -> div (ToastTitle)
    TOAST_TITLE = "ol li div.text-sm.font-semibold"
    TOAST_DESC = "ol li div.text-sm.opacity-90"

    # --- Helper Methods for Shadcn Components ---

    def _select_option(self, label_text, option_text):
        """
        Handles Radix UI Select (Used for Account Type)
        """
        trigger = self.page.locator(f"div.space-y-2:has(label:has-text('{label_text}')) button[role='combobox']")
        trigger.click()
        self.page.get_by_role("option", name=option_text).click()

    # --- Actions ---

    @allure.step("Enter account holder name")
    def enter_name(self, name):
        self.fill(self.NAME_INPUT, name)

    @allure.step("Enter date of birth")
    def enter_dob(self, dob):
        self.fill(self.DOB_INPUT, dob)

    @allure.step("Select gender")
    def select_gender(self, gender):
        # CHANGED: Now targets RadioGroup Item (button with role='radio')
        # We target by the 'value' attribute which we set to "Male", "Female", etc.
        self.click(f"button[role='radio'][value='{gender}']")

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
        self._select_option("Account Type", account_type)

    @allure.step("Enter initial balance")
    def enter_balance(self, balance):
        self.fill(self.BALANCE_INPUT, balance)

    @allure.step("Select services")
    def select_services(self, services):
        if services:
            for service in services.split(","):
                self.page.get_by_label(service.strip()).click()

    @allure.step("Set marketing opt-in")
    def set_marketing_opt_in(self, opt_in):
        if str(opt_in).lower() == "true":
            self.page.get_by_label("Marketing Communications").click()

    @allure.step("Accept terms and conditions")
    def accept_terms(self):
        self.page.get_by_label("Terms and Conditions").click()

    @allure.step("Submit create account form")
    def submit_form_and_capture_account_id(self) -> tuple[str, str, str]:
        self.click(self.SUBMIT_BTN)

        # 1. Capture Toast Message
        # We wait for the toast title to appear. Shadcn toasts usually persist
        # across the immediate route change in a SPA.

        self.page.wait_for_selector(self.TOAST_TITLE, state="visible")
        toast_text = self.get_text(self.TOAST_TITLE)
        toast_desc = self.get_text(self.TOAST_DESC)

        # 2. Wait for URL Redirection to Account Details
        self.page.wait_for_url(re.compile(r".*/account-details/\d+"))

        # 3. Extract ID from URL
        current_url = self.page.url
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

    def get_validation_message_for_field(self, field_name: str) -> str:
        locator_map = {
            "name": self.NAME_INPUT,
            "dob": self.DOB_INPUT,
            "email": self.EMAIL_INPUT,
            "phone": self.PHONE_INPUT,
            "balance": self.BALANCE_INPUT
        }
        if field_name not in locator_map:
            raise ValueError(f"Field '{field_name}' validation check not supported")
        return self.get_validation_message(locator_map[field_name])