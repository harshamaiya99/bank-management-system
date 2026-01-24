import allure
from tests.web_selenium.pages.base_page import BasePage


from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class DetailsPage(BasePage):
    # --- Locators ---
    ID_FIELD = "#accountId"
    NAME_INPUT = "#accountHolderName"
    DOB_INPUT = "#dob"
    GENDER_RADIO = "input[name='gender']"
    EMAIL_INPUT = "#email"
    PHONE_INPUT = "#phone"
    ADDRESS_INPUT = "#address"
    ZIP_INPUT = "#zipCode"
    TYPE_SELECT = "#accountType"
    BALANCE_INPUT = "#balance"
    STATUS_SELECT = "#status"
    SERVICE_CHECKBOX = "input[name='services']"
    MARKETING_CHK = "#marketingOptIn"
    UPDATE_BTN = ".btn-update"
    DELETE_BTN = ".btn-delete"
    LOADING_MSG = "#loadingMessage"
    ERROR_MSG = "#errorMessage"

    # --- Actions & Getters ---

    @allure.step("Wait for details to load")
    def wait_for_details_to_load(self):
        # 'find' automatically waits for visibility based on BasePage logic
        self.find(self.ID_FIELD)

    @allure.step("Get account_id")
    def get_account_id(self):
        return self.get_input_value(self.ID_FIELD)

    @allure.step("Get account holder name")
    def get_name(self):
        return self.get_input_value(self.NAME_INPUT)

    @allure.step("Get dob")
    def get_dob(self):
        return self.get_input_value(self.DOB_INPUT)

    @allure.step("Get email")
    def get_email(self):
        return self.get_input_value(self.EMAIL_INPUT)

    @allure.step("Get phone no")
    def get_phone(self):
        return self.get_input_value(self.PHONE_INPUT)

    @allure.step("Get address")
    def get_address(self):
        return self.get_input_value(self.ADDRESS_INPUT)

    @allure.step("Get ZIP")
    def get_zip(self):
        return self.get_input_value(self.ZIP_INPUT)

    @allure.step("Get account type")
    def get_account_type(self):
        return self.get_input_value(self.TYPE_SELECT)

    @allure.step("Get balance")
    def get_balance(self):
        return self.get_input_value(self.BALANCE_INPUT)

    @allure.step("Get marketing_opt_in")
    def get_marketing_opt_in(self):
        # Uses BasePage's is_checked() wrapper
        is_marketing_checked = self.is_checked(self.MARKETING_CHK)
        return "true" if is_marketing_checked else "false"

    @allure.step("Get gender")
    def get_gender(self):
        # CSS selector :checked works in Selenium to find the selected radio
        return self.find(f"{self.GENDER_RADIO}:checked").get_attribute("value")

    @allure.step("Get status")
    def get_status(self):
        return self.get_input_value(self.STATUS_SELECT)

    @allure.step("Get services")
    def get_services(self):
        # 1. Find all checked service checkboxes
        checked_elements = self.find_all(f"{self.SERVICE_CHECKBOX}:checked")
        # 2. Extract value attributes
        values = [el.get_attribute("value") for el in checked_elements]
        # 3. Join with commas to match CSV format
        return ",".join(values)

    # --- Update Methods ---

    @allure.step("Update account holder name")
    def update_name(self, updated_name):
        self.fill(self.NAME_INPUT, updated_name)

    @allure.step("Update dob")
    def update_dob(self, updated_dob):
        # *** FIX: Use JS to bypass date input mask issues in Selenium ***
        self.set_value_js(self.DOB_INPUT, updated_dob)

    @allure.step("Update email")
    def update_email(self, updated_email):
        self.fill(self.EMAIL_INPUT, updated_email)

    @allure.step("Update phone no")
    def update_phone(self, updated_phone):
        self.fill(self.PHONE_INPUT, updated_phone)

    @allure.step("Update address")
    def update_address(self, updated_address):
        self.fill(self.ADDRESS_INPUT, updated_address)

    @allure.step("Update ZIP")
    def update_zip(self, updated_zip_code):
        self.fill(self.ZIP_INPUT, updated_zip_code)

    @allure.step("Update account type")
    def update_account_type(self, updated_account_type):
        self.select_option(self.TYPE_SELECT, updated_account_type)

    @allure.step("Update balance")
    def update_balance(self, updated_balance):
        self.fill(self.BALANCE_INPUT, updated_balance)

    @allure.step("Update gender")
    def update_gender(self, updated_gender):
        self.click(f"{self.GENDER_RADIO}[value='{updated_gender}']")

    @allure.step("Update status")
    def update_status(self, updated_status):
        self.select_option(self.STATUS_SELECT, updated_status)

    @allure.step("Update services")
    def update_services(self, services):
        # 1. Uncheck all currently selected services
        all_checkboxes = self.find_all(self.SERVICE_CHECKBOX)
        for checkbox in all_checkboxes:
            if checkbox.is_selected():
                checkbox.click()

        # 2. Check only the services provided
        if services:
            for service in services.split(","):
                # Use standard check method for specific value
                self.check(f"{self.SERVICE_CHECKBOX}[value='{service.strip()}']")

    @allure.step("Update marketing opt-in")
    def update_marketing_opt_in(self, opt_in):
        if opt_in == "true":
            self.check(self.MARKETING_CHK)
        elif opt_in == "false":
            self.uncheck(self.MARKETING_CHK)

    @allure.step("Click on Update button")
    def update_account(self) -> str:
        self.click(self.UPDATE_BTN)

        alert = WebDriverWait(self.driver, 5).until(EC.alert_is_present())
        alert_text = alert.text
        alert.accept()

        self.wait_for_url("/")

        return alert_text

    @allure.step("Click on Delete account button")
    def delete_account(self):
        # Click delete
        self.click(self.DELETE_BTN)

        # Handle confirm()
        confirm = WebDriverWait(self.driver, 5).until(EC.alert_is_present())
        confirm.accept()

        # Handle alert()
        alert = WebDriverWait(self.driver, 5).until(EC.alert_is_present())
        alert.accept()

        # Wait for redirect
        self.wait_for_url("/")

    # --- Aggregated Logic ---

    def update_account_details(self, data: dict) -> str:
        self.update_name(data["updated_account_holder_name"])
        self.update_dob(data["updated_dob"])
        self.update_gender(data["updated_gender"])
        self.update_email(data["updated_email"])
        self.update_phone(data["updated_phone"])
        self.update_address(data["updated_address"])
        self.update_zip(data["updated_zip_code"])
        self.update_account_type(data["updated_account_type"])
        self.update_balance(data["updated_balance"])
        self.update_status(data["updated_status"])
        self.update_services(data["updated_services"])
        self.update_marketing_opt_in(data["updated_marketing_opt_in"])
        return self.update_account()  # Return the success message

    def get_account_details_as_dict(self) -> dict:
        """
        Scrapes all relevant fields from the Details page and returns them as a dictionary.
        """
        self.wait_for_details_to_load()

        return {
            "account_id": self.get_account_id(),
            "account_holder_name": self.get_name(),
            "dob": self.get_dob(),
            "gender": self.get_gender(),
            "email": self.get_email(),
            "phone": self.get_phone(),
            "address": self.get_address(),
            "zip_code": self.get_zip(),
            "account_type": self.get_account_type(),
            "balance": self.get_balance(),
            "status": self.get_status(),
            "services": self.get_services(),
            "marketing_opt_in": self.get_marketing_opt_in()
        }