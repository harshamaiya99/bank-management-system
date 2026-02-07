import allure
import re
from playwright.sync_api import Page, expect


class CreatePage:
    def __init__(self, page: Page):
        self.page = page

    # Standard Inputs
    NAME_INPUT = "input[name='account_holder_name']"
    DOB_INPUT = "input[name='dob']"
    EMAIL_INPUT = "input[name='email']"
    PHONE_INPUT = "input[name='phone']"
    ADDRESS_INPUT = "input[name='address']"
    ZIP_INPUT = "input[name='zip_code']"
    BALANCE_INPUT = "input[name='balance']"

    SUBMIT_BTN = "button[type='submit']"

    # Targets the first and second child divs inside the Toast Grid
    # 'ol li' -> The Toast Item
    # '.grid' -> The container defined in Toaster.tsx
    # 'div:nth-child(1)' -> The Title
    TOAST_TITLE = "ol li .grid > div:nth-child(1)"
    # 'div:nth-child(2)' -> The Description
    TOAST_DESC = "ol li .grid > div:nth-child(2)"

    # --- Actions ---

    @allure.step("Enter account holder name")
    def enter_name(self, name):
        self.page.locator(self.NAME_INPUT).fill(name)

    @allure.step("Enter date of birth")
    def enter_dob(self, dob):
        self.page.locator(self.DOB_INPUT).fill(dob)

    @allure.step("Select gender")
    def select_gender(self, gender):
        # targets RadioGroup Item (button with role='radio')
        # We target by the 'value' attribute which we set to "Male", "Female", etc.
        self.page.locator(f"button[role='radio'][value='{gender}']").click()

    @allure.step("Enter email")
    def enter_email(self, email):
        self.page.locator(self.EMAIL_INPUT).fill(email)

    @allure.step("Enter phone number")
    def enter_phone(self, phone):
        self.page.locator(self.PHONE_INPUT).fill(phone)

    @allure.step("Enter address")
    def enter_address(self, address):
        self.page.locator(self.ADDRESS_INPUT).fill(address)

    @allure.step("Enter zip code")
    def enter_zip(self, zip_code):
        self.page.locator(self.ZIP_INPUT).fill(zip_code)

    @allure.step("Select account type")
    def select_account_type(self, account_type):
        # 1. Click the trigger identified by its Label
        self.page.get_by_role("combobox", name="Account Type").click()

        # 2. Click the option
        self.page.get_by_role("option", name=account_type).click()

    @allure.step("Enter initial balance")
    def enter_balance(self, balance):
        self.page.locator(self.BALANCE_INPUT).fill(balance)

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
        self.page.locator(self.SUBMIT_BTN).click()

        # 1. Capture Toast Message
        # We wait for the toast title to appear.

        self.page.locator(self.TOAST_TITLE).wait_for(state="visible")
        toast_text = self.page.locator(self.TOAST_TITLE).text_content()
        toast_desc = self.page.locator(self.TOAST_DESC).text_content()

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