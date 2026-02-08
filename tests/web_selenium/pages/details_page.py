import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tests.web_selenium.utils.actions import smart_fill, smart_click, smart_check, smart_uncheck, get_text, get_value


class DetailsPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    NAME_INPUT = (By.NAME, "account_holder_name")
    DOB_INPUT = (By.NAME, "dob")
    EMAIL_INPUT = (By.NAME, "email")
    PHONE_INPUT = (By.NAME, "phone")
    ADDRESS_INPUT = (By.NAME, "address")
    ZIP_INPUT = (By.NAME, "zip_code")
    BALANCE_INPUT = (By.NAME, "balance")

    UPDATE_BTN = (By.XPATH, "//button[contains(., 'Save Changes')]")
    DELETE_BTN = (By.XPATH, "//button[contains(., 'Delete Account')]")
    CONFIRM_DELETE_BTN = (By.XPATH, "//div[@role='alertdialog']//button[contains(., 'Delete Account')]")

    TOAST_TITLE = (By.CSS_SELECTOR, "ol li .grid > div:nth-child(1)")
    TOAST_DESC = (By.CSS_SELECTOR, "ol li .grid > div:nth-child(2)")

    SERVICE_OPTIONS = ["Internet Banking", "Debit Card", "Cheque Book", "SMS Alerts"]

    @allure.step("Wait for details to load")
    def wait_for_details_to_load(self):
        self.wait.until(EC.visibility_of_element_located(self.NAME_INPUT))

    # --- Getters ---
    @allure.step("Get account_id")
    def get_account_id(self):
        element = self.wait.until(EC.visibility_of_element_located((By.XPATH, "//*[contains(text(), 'ID: ')]")))
        return element.text.replace("ID: ", "").strip()

    @allure.step("Get account holder name")
    def get_name(self):
        return get_value(self.driver, self.NAME_INPUT)

    @allure.step("Get dob")
    def get_dob(self):
        return get_value(self.driver, self.DOB_INPUT)

    @allure.step("Get gender")
    def get_gender(self):
        # Find the button that is aria-checked=true
        el = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "button[role='radio'][aria-checked='true']")))
        return el.get_attribute("value")

    @allure.step("Get email")
    def get_email(self):
        return get_value(self.driver, self.EMAIL_INPUT)

    @allure.step("Get phone")
    def get_phone(self):
        return get_value(self.driver, self.PHONE_INPUT)

    @allure.step("Get address")
    def get_address(self):
        return get_value(self.driver, self.ADDRESS_INPUT)

    @allure.step("Get zip")
    def get_zip(self):
        return get_value(self.driver, self.ZIP_INPUT)

    @allure.step("Get account type")
    def get_account_type(self):
        locator = (By.XPATH, "//label[contains(., 'Account Type')]/following::input[1]")
        return self.wait.until(EC.presence_of_element_located(locator)).get_attribute("value")

    @allure.step("Get status")
    def get_status(self):
        trigger = (By.XPATH, "//label[contains(., 'Account Status')]/following::button[@role='combobox'][1]")
        return get_text(self.driver, trigger)

    @allure.step("Get balance")
    def get_balance(self):
        return get_value(self.driver, self.BALANCE_INPUT)

    @allure.step("Get services")
    def get_services(self):
        active_services = []
        for service in self.SERVICE_OPTIONS:
            text = service.strip()
            label_el = self.wait.until(EC.presence_of_element_located((By.XPATH, f"//label[contains(., '{text}')]")))
            target_id = label_el.get_attribute("for")

            if target_id:
                locator = (By.ID, target_id)
            else:
                locator = (By.XPATH, f"//label[contains(., '{text}')]//button[@role='checkbox']")

            element = self.driver.find_element(*locator)
            if element.get_attribute("aria-checked") == "true":
                active_services.append(service)
        return ",".join(active_services)

    @allure.step("Get marketing_opt_in")
    def get_marketing_opt_in(self):
        text = "Marketing Communications"
        label_el = self.wait.until(EC.presence_of_element_located((By.XPATH, f"//label[contains(., '{text}')]")))
        target_id = label_el.get_attribute("for")

        if target_id:
            locator = (By.ID, target_id)
        else:
            locator = (By.XPATH, f"//label[contains(., '{text}')]//button[@role='checkbox']")

        is_checked = self.driver.find_element(*locator).get_attribute("aria-checked") == "true"
        return "true" if is_checked else "false"

    # --- Updaters ---
    @allure.step("Update account holder name")
    def update_name(self, name):
        smart_fill(self.driver, self.NAME_INPUT, name)

    @allure.step("Update dob")
    def update_dob(self, dob):
        smart_fill(self.driver, self.DOB_INPUT, dob)

    @allure.step("Update gender")
    def update_gender(self, gender):
        smart_click(self.driver, (By.CSS_SELECTOR, f"button[role='radio'][value='{gender}']"))

    @allure.step("Update email")
    def update_email(self, email):
        smart_fill(self.driver, self.EMAIL_INPUT, email)

    @allure.step("Update phone")
    def update_phone(self, phone):
        smart_fill(self.driver, self.PHONE_INPUT, phone)

    @allure.step("Update address")
    def update_address(self, address):
        smart_fill(self.driver, self.ADDRESS_INPUT, address)

    @allure.step("Update zip")
    def update_zip(self, zip_code):
        smart_fill(self.driver, self.ZIP_INPUT, zip_code)

    @allure.step("Update balance")
    def update_balance(self, balance):
        smart_fill(self.driver, self.BALANCE_INPUT, balance)

    @allure.step("Update status")
    def update_status(self, status):
        trigger = (By.XPATH, "//label[contains(., 'Account Status')]/following::button[@role='combobox'][1]")
        smart_click(self.driver, trigger)

        option = (By.XPATH, f"//div[@role='option']//span[contains(text(), '{status}')]")
        smart_click(self.driver, option)

    @allure.step("Update services")
    def update_services(self, services_str):
        # 1. Uncheck all first
        for service in self.SERVICE_OPTIONS:
            text = service.strip()
            label_el = self.wait.until(EC.presence_of_element_located((By.XPATH, f"//label[contains(., '{text}')]")))
            target_id = label_el.get_attribute("for")

            if target_id:
                locator = (By.ID, target_id)
            else:
                locator = (By.XPATH, f"//label[contains(., '{text}')]//button[@role='checkbox']")

            smart_uncheck(self.driver, locator)

        # 2. Check requested
        if services_str:
            for service in services_str.split(","):
                text = service.strip()
                label_el = self.wait.until(
                    EC.presence_of_element_located((By.XPATH, f"//label[contains(., '{text}')]")))
                target_id = label_el.get_attribute("for")

                if target_id:
                    locator = (By.ID, target_id)
                else:
                    locator = (By.XPATH, f"//label[contains(., '{text}')]//button[@role='checkbox']")

                smart_check(self.driver, locator)

    @allure.step("Update marketing")
    def update_marketing_opt_in(self, marketing_check):
        text = "Marketing Communications"
        label_el = self.wait.until(EC.presence_of_element_located((By.XPATH, f"//label[contains(., '{text}')]")))
        target_id = label_el.get_attribute("for")

        if target_id:
            locator = (By.ID, target_id)
        else:
            locator = (By.XPATH, f"//label[contains(., '{text}')]//button[@role='checkbox']")

        should_check = str(marketing_check).lower() == "true"
        if should_check:
            smart_check(self.driver, locator)
        else:
            smart_uncheck(self.driver, locator)

    @allure.step("Click on Update button")
    def update_account(self) -> tuple[str, str]:
        smart_click(self.driver, self.UPDATE_BTN)
        toast_text = get_text(self.driver, self.TOAST_TITLE)
        toast_desc = get_text(self.driver, self.TOAST_DESC)
        return toast_text, toast_desc

    @allure.step("Click on Delete account button")
    def delete_account(self):
        smart_click(self.driver, self.DELETE_BTN)
        smart_click(self.driver, self.CONFIRM_DELETE_BTN)

        toast_text = get_text(self.driver, self.TOAST_TITLE)
        toast_desc = get_text(self.driver, self.TOAST_DESC)

        self.wait.until(EC.url_contains("/dashboard"))
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