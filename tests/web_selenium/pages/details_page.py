import allure
from selenium.webdriver.common.by import By
from tests.web_selenium.pages.base_page import BasePage


class DetailsPage(BasePage):
    # --- Locators (Tuples) ---
    ID_FIELD = (By.ID, "accountId")
    NAME_INPUT = (By.ID, "accountHolderName")
    DOB_INPUT = (By.ID, "dob")

    # Generic locators for groups
    GENDER_CHECKED = (By.CSS_SELECTOR, "input[name='gender']:checked")
    SERVICE_CHECKED = (By.CSS_SELECTOR, "input[name='services']:checked")
    SERVICE_ALL = (By.CSS_SELECTOR, "input[name='services']")

    EMAIL_INPUT = (By.ID, "email")
    PHONE_INPUT = (By.ID, "phone")
    ADDRESS_INPUT = (By.ID, "address")
    ZIP_INPUT = (By.ID, "zipCode")
    TYPE_SELECT = (By.ID, "accountType")
    BALANCE_INPUT = (By.ID, "balance")
    STATUS_SELECT = (By.ID, "status")
    MARKETING_CHK = (By.ID, "marketingOptIn")

    UPDATE_BTN = (By.CSS_SELECTOR, ".btn-update")
    DELETE_BTN = (By.CSS_SELECTOR, ".btn-delete")
    LOADING_MSG = (By.ID, "loadingMessage")
    ERROR_MSG = (By.ID, "errorMessage")

    # --- Actions & Getters ---

    @allure.step("Wait for details to load")
    def wait_for_details_to_load(self):
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
        is_checked = self.is_checked(self.MARKETING_CHK)
        return "true" if is_checked else "false"

    @allure.step("Get gender")
    def get_gender(self):
        return self.find(self.GENDER_CHECKED).get_attribute("value")

    @allure.step("Get status")
    def get_status(self):
        return self.get_input_value(self.STATUS_SELECT)

    @allure.step("Get services")
    def get_services(self):
        checked_elements = self.find_all(self.SERVICE_CHECKED)
        values = [el.get_attribute("value") for el in checked_elements]
        return ",".join(values)

    # --- Update Methods ---

    @allure.step("Update account holder name")
    def update_name(self, updated_name):
        self.fill(self.NAME_INPUT, updated_name)

    @allure.step("Update dob")
    def update_dob(self, updated_dob):
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
        locator = (By.CSS_SELECTOR, f"input[name='gender'][value='{updated_gender}']")
        self.click(locator)

    @allure.step("Update status")
    def update_status(self, updated_status):
        self.select_option(self.STATUS_SELECT, updated_status)

    @allure.step("Update services")
    def update_services(self, services):
        # 1. Uncheck all
        all_checkboxes = self.find_all(self.SERVICE_ALL)
        for checkbox in all_checkboxes:
            if checkbox.is_selected():
                checkbox.click()

        # 2. Check provided
        if services:
            for service in services.split(","):
                locator = (By.CSS_SELECTOR, f"input[name='services'][value='{service.strip()}']")
                self.check(locator)

    @allure.step("Update marketing opt-in")
    def update_marketing_opt_in(self, opt_in):
        if opt_in == "true":
            self.check(self.MARKETING_CHK)
        elif opt_in == "false":
            self.uncheck(self.MARKETING_CHK)

    @allure.step("Click on Update button")
    def update_account(self) -> str:
        self.click(self.UPDATE_BTN)
        alert_text = self.get_alert_text() or ""
        self.wait_for_url("/")
        return alert_text

    @allure.step("Click on Delete account button")
    def delete_account(self):
        self.click(self.DELETE_BTN)

        # Confirm delete
        self.get_alert_text()

        # Success message
        self.get_alert_text()

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
        return self.update_account()

    def get_account_details_as_dict(self) -> dict:
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