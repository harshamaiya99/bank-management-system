import allure
from playwright.sync_api import Page, expect


class DetailsPage:
    def __init__(self, page: Page):
        self.page = page

    ID_TEXT_LOCATOR = "p.text-muted-foreground.font-mono"
    NAME_INPUT = "input[name='account_holder_name']"
    DOB_INPUT = "input[name='dob']"
    EMAIL_INPUT = "input[name='email']"
    PHONE_INPUT = "input[name='phone']"
    ADDRESS_INPUT = "input[name='address']"
    ZIP_INPUT = "input[name='zip_code']"
    BALANCE_INPUT = "input[name='balance']"

    UPDATE_BTN = "button:has-text('Save Changes')"
    DELETE_BTN = "button:has-text('Delete Account')"
    CONFIRM_DELETE_BTN = "div[role='alertdialog'] button:has-text('Delete Account')"

    # Define known options to iterate safely
    SERVICE_OPTIONS = ["Internet Banking", "Debit Card", "Cheque Book", "SMS Alerts"]

    # Targets the first and second child divs inside the Toast Grid
    # 'ol li' -> The Toast Item
    # '.grid' -> The container defined in Toaster.tsx
    # 'div:nth-child(1)' -> The Title
    TOAST_TITLE = "ol li .grid > div:nth-child(1)"
    # 'div:nth-child(2)' -> The Description
    TOAST_DESC = "ol li .grid > div:nth-child(2)"

    @allure.step("Wait for details to load")
    def wait_for_details_to_load(self):
        self.page.wait_for_selector(self.NAME_INPUT, state="visible")

    # --- Getters ---

    @allure.step("Get account_id")
    def get_account_id(self):
        text = self.page.locator(self.ID_TEXT_LOCATOR).text_content()
        return text.replace("ID: ", "").strip()

    @allure.step("Get account holder name")
    def get_name(self):
        return self.page.locator(self.NAME_INPUT).input_value()

    @allure.step("Get dob")
    def get_dob(self):
        return self.page.locator(self.DOB_INPUT).input_value()

    @allure.step("Get gender")
    def get_gender(self):
        return self.page.locator("button[role='radio'][aria-checked='true']").get_attribute("value")

    @allure.step("Get email")
    def get_email(self):
        return self.page.locator(self.EMAIL_INPUT).input_value()

    @allure.step("Get phone")
    def get_phone(self):
        return self.page.locator(self.PHONE_INPUT).input_value()

    @allure.step("Get address")
    def get_address(self):
        return self.page.locator(self.ADDRESS_INPUT).input_value()

    @allure.step("Get zip")
    def get_zip(self):
        return self.page.locator(self.ZIP_INPUT).input_value()

    @allure.step("Get account type")
    def get_account_type(self):
        return self.page.get_by_role("textbox", name="Account Type").input_value()

    @allure.step("Get status")
    def get_status(self):
        return self.page.get_by_role("combobox", name="Account Status").text_content()

    @allure.step("Get balance")
    def get_balance(self):
        return self.page.locator(self.BALANCE_INPUT).input_value()

    @allure.step("Get services")
    def get_services(self):
        active_services = []
        for service in self.SERVICE_OPTIONS:
            # Check if specific service checkbox is checked
            if self.page.get_by_role("checkbox", name=service).get_attribute("aria-checked") == "true":
                active_services.append(service)
        return ",".join(active_services)

    @allure.step("Get marketing_opt_in")
    def get_marketing_opt_in(self):
        is_checked = self.page.get_by_role("checkbox", name="Marketing Communications").get_attribute(
            "aria-checked") == "true"
        return "true" if is_checked else "false"

    # --- Updaters ---
    @allure.step("Update account holder name")
    def update_name(self, name):
        self.page.locator(self.NAME_INPUT).fill(name)

    @allure.step("Update dob")
    def update_dob(self, dob):
        self.page.locator(self.DOB_INPUT).fill(dob)

    @allure.step("Update gender")
    def update_gender(self, gender):
        self.page.locator(f"button[role='radio'][value='{gender}']").click()

    @allure.step("Update email")
    def update_email(self, email):
        self.page.locator(self.EMAIL_INPUT).fill(email)

    @allure.step("Update phone")
    def update_phone(self, phone):
        self.page.locator(self.PHONE_INPUT).fill(phone)

    @allure.step("Update address")
    def update_address(self, address):
        self.page.locator(self.ADDRESS_INPUT).fill(address)

    @allure.step("Update zip")
    def update_zip(self, zip_code):
        self.page.locator(self.ZIP_INPUT).fill(zip_code)

    @allure.step("Update balance")
    def update_balance(self, balance):
        self.page.locator(self.BALANCE_INPUT).fill(balance)

    @allure.step("Update status")
    def update_status(self, status):
        # 1. Click the trigger identified by its Label
        self.page.get_by_role("combobox", name="Account Status").click()

        # 2. Click the option
        self.page.get_by_role("option", name=status).click()

    @allure.step("Update services")
    def update_services(self, services_str):
        # 1. Uncheck all services first to have a clean state
        for service in self.SERVICE_OPTIONS:
            box = self.page.get_by_role("checkbox", name=service)
            if box.get_attribute("aria-checked") == "true":
                box.click()

        # 2. Check the requested services
        if services_str:
            for service in services_str.split(","):
                # Click only if not already checked (though we just unchecked all, safe to just click)
                self.page.get_by_role("checkbox", name=service.strip()).click()

    @allure.step("Update marketing")
    def update_marketing_opt_in(self, marketing_check):
        box = self.page.get_by_role("checkbox", name="Marketing Communications")
        is_checked = box.get_attribute("aria-checked") == "true"
        should_check = str(marketing_check).lower() == "true"

        if is_checked != should_check:
            box.click()


    @allure.step("Click on Update button")
    def update_account(self) -> tuple[str, str]:
        self.page.locator(self.UPDATE_BTN).click()

        self.page.wait_for_selector(self.TOAST_TITLE, state="visible")
        toast_text = self.page.locator(self.TOAST_TITLE).text_content()
        toast_desc = self.page.locator(self.TOAST_DESC).text_content()

        return toast_text, toast_desc

    @allure.step("Click on Delete account button")
    def delete_account(self):
        self.page.locator(self.DELETE_BTN).click()
        self.page.locator(self.CONFIRM_DELETE_BTN).click()

        self.page.wait_for_selector(self.TOAST_TITLE, state="visible")
        toast_text = self.page.locator(self.TOAST_TITLE).text_content()
        toast_desc = self.page.locator(self.TOAST_DESC).text_content()

        self.page.wait_for_url("**/dashboard")
        return toast_text, toast_desc

    def update_account_details(self, data: dict) -> tuple[str, str]:
        self.update_name(data["updated_account_holder_name"])
        self.update_dob(data["updated_dob"])
        self.update_gender(data["updated_gender"])
        self.update_email(data["updated_email"])
        self.update_phone(data["updated_phone"])
        self.update_address(data["updated_address"])
        self.update_zip(data["updated_zip_code"])
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