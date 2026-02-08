import allure
import re
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tests.web_selenium.utils.actions import smart_fill, smart_click, smart_check, smart_uncheck, get_text


class CreatePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    # Standard Inputs
    NAME_INPUT = (By.NAME, "account_holder_name")
    DOB_INPUT = (By.NAME, "dob")
    EMAIL_INPUT = (By.NAME, "email")
    PHONE_INPUT = (By.NAME, "phone")
    ADDRESS_INPUT = (By.NAME, "address")
    ZIP_INPUT = (By.NAME, "zip_code")
    BALANCE_INPUT = (By.NAME, "balance")
    SUBMIT_BTN = (By.CSS_SELECTOR, "button[type='submit']")

    TOAST_TITLE = (By.CSS_SELECTOR, "ol li .grid > div:nth-child(1)")
    TOAST_DESC = (By.CSS_SELECTOR, "ol li .grid > div:nth-child(2)")

    @allure.step("Enter account holder name")
    def enter_name(self, name):
        smart_fill(self.driver, self.NAME_INPUT, name)

    @allure.step("Enter date of birth")
    def enter_dob(self, dob):
        smart_fill(self.driver, self.DOB_INPUT, dob)

    @allure.step("Select gender")
    def select_gender(self, gender):
        locator = (By.CSS_SELECTOR, f"button[role='radio'][value='{gender}']")
        smart_click(self.driver, locator)

    @allure.step("Enter email")
    def enter_email(self, email):
        smart_fill(self.driver, self.EMAIL_INPUT, email)

    @allure.step("Enter phone number")
    def enter_phone(self, phone):
        smart_fill(self.driver, self.PHONE_INPUT, phone)

    @allure.step("Enter address")
    def enter_address(self, address):
        smart_fill(self.driver, self.ADDRESS_INPUT, address)

    @allure.step("Enter zip code")
    def enter_zip(self, zip_code):
        smart_fill(self.driver, self.ZIP_INPUT, zip_code)

    @allure.step("Select account type")
    def select_account_type(self, account_type):
        # Trigger
        trigger = (By.XPATH, "//label[contains(., 'Account Type')]/following::button[@role='combobox'][1]")
        smart_click(self.driver, trigger)

        # Option
        option = (By.XPATH, f"//div[@role='option']//span[contains(text(), '{account_type}')]")
        smart_click(self.driver, option)

    @allure.step("Enter initial balance")
    def enter_balance(self, balance):
        smart_fill(self.driver, self.BALANCE_INPUT, balance)

    @allure.step("Select services")
    def select_services(self, services):
        if services:
            for service in services.split(","):
                text = service.strip()
                # Find Label
                label_el = self.wait.until(
                    EC.visibility_of_element_located((By.XPATH, f"//label[contains(., '{text}')]")))
                target_id = label_el.get_attribute("for")

                if target_id:
                    locator = (By.ID, target_id)
                else:
                    locator = (By.XPATH, f"//label[contains(., '{text}')]//button[@role='checkbox']")

                smart_check(self.driver, locator)

    @allure.step("Set marketing opt-in")
    def set_marketing_opt_in(self, opt_in):
        text = "Marketing Communications"
        label_el = self.wait.until(EC.visibility_of_element_located((By.XPATH, f"//label[contains(., '{text}')]")))
        target_id = label_el.get_attribute("for")

        if target_id:
            locator = (By.ID, target_id)
        else:
            locator = (By.XPATH, f"//label[contains(., '{text}')]//button[@role='checkbox']")

        if str(opt_in).lower() == "true":
            smart_check(self.driver, locator)
        else:
            smart_uncheck(self.driver, locator)

    @allure.step("Accept terms and conditions")
    def accept_terms(self):
        text = "Terms and Conditions"
        label_el = self.wait.until(EC.visibility_of_element_located((By.XPATH, f"//label[contains(., '{text}')]")))
        target_id = label_el.get_attribute("for")

        if target_id:
            locator = (By.ID, target_id)
        else:
            locator = (By.XPATH, f"//label[contains(., '{text}')]//button[@role='checkbox']")

        smart_check(self.driver, locator)

    @allure.step("Submit create account form")
    def submit_form_and_capture_account_id(self) -> tuple[str, str, str]:
        smart_click(self.driver, self.SUBMIT_BTN)

        toast_text = get_text(self.driver, self.TOAST_TITLE)
        toast_desc = get_text(self.driver, self.TOAST_DESC)

        # Longer wait for backend processing
        WebDriverWait(self.driver, 15).until(EC.url_contains("/account-details/"))

        current_url = self.driver.current_url
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