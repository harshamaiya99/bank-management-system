import allure
from tests.web.pages.base_page import BasePage


class DetailsPage(BasePage):
    # Locators
    ID_FIELD = "#accountId"
    NAME_INPUT = "#accountHolderName"
    DOB_INPUT = "#dob"
    EMAIL_INPUT = "#email"
    PHONE_INPUT = "#phone"
    ADDRESS_INPUT = "#address"
    ZIP_INPUT = "#zipCode"
    TYPE_SELECT = "#accountType"
    BALANCE_INPUT = "#balance"
    MARKETING_CHK = "#marketingOptIn"
    UPDATE_BTN = ".btn-update"
    DELETE_BTN = ".btn-delete"
    LOADING_MSG = "#loadingMessage"
    ERROR_MSG = "#errorMessage"


    @allure.step("Wait for details to load")
    def wait_for_details_to_load(self):
        self.page.wait_for_selector(self.ID_FIELD, state="visible")

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
        return self.get_input_value(self.MARKETING_CHK)



    @allure.step("Update account holder name")
    def update_name(self, updated_name):
        self.fill(self.NAME_INPUT, updated_name)

    @allure.step("Update dob")
    def update_dob(self, updated_dob):
        self.fill(self.DOB_INPUT, updated_dob)

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

    # @allure.step("Update marketing_opt_in")
    # def update_marketing_opt_in(self, updated_marketing_opt_in):
    #     self.fill(self.MARKETING_CHK, updated_marketing_opt_in)

    @allure.step("Click on Update button")
    def update_account(self):
        # Handle alert for update
        self.page.once("dialog", lambda d: d.accept())
        self.click(self.UPDATE_BTN)
        self.page.wait_for_load_state("networkidle")



    def get_error_message(self):
        """Waits for the error message to be visible and returns its text."""
        self.page.wait_for_selector(self.ERROR_MSG, state="visible")
        return self.get_text(self.ERROR_MSG)

    def get_account_details(self):
        self.wait_for_details_to_load()
        self.get_account_id()
        self.get_name()
        self.get_dob()
        # self.get_gender()
        self.get_email()
        self.get_phone()
        self.get_address()
        self.get_zip()
        self.get_account_type()
        self.get_balance()
        # self.get_services()
        self.get_marketing_opt_in()

    def update_account_details(self, data: dict) -> None:
        self.update_name(data["updated_account_holder_name"])
        self.update_dob(data["updated_dob"])
        # self.select_gender(data["updated_gender"])
        self.update_email(data["updated_email"])
        self.update_phone(data["updated_phone"])
        self.update_address(data["updated_address"])
        self.update_zip(data["updated_zip_code"])
        self.update_account_type(data["updated_account_type"])
        self.update_balance(data["updated_balance"])
        # self.select_services(data["updated_services"])
        # self.update_marketing_opt_in(data["updated_marketing_opt_in"])
        self.update_account()

    @allure.step("Delete account")
    def delete_account(self):
        # Handle confirmation alert
        self.page.once("dialog", lambda d: d.accept())
        self.click(self.DELETE_BTN)
        self.page.wait_for_load_state("networkidle")
