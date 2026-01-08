import pytest
import allure
import os
from tests.web.utils.csv_reader import read_csv_data

TEST_DATA_FILE = os.path.join(os.path.dirname(__file__), "data", "test_data_negative.csv")


@allure.epic("Web UI")
@allure.feature("Negative Scenarios")
@pytest.mark.parametrize("row", read_csv_data(TEST_DATA_FILE), ids=lambda r: r["tc_name"])
def test_negative_scenarios(home_page, create_page, details_page, row):
    """
    Handles multiple negative testing contexts:
    1. home_search: Validation on the Home Page search bar (DOM text).
    2. detail_search: Logic verification (Account not found Alert).
    3. create_account: Backend/Form validation (Form submission Alert).
    """

    # --- Context 1: Home Page Search Validation ---
    if row["test_context"] == "home_search":
        with allure.step(f"Testing Home Search Validation: {row['tc_name']}"):
            home_page.navigate_to_home()
            home_page.search_account(row["account_id"])
            assert home_page.get_error_message() == row["expected_message"]

    # --- Context 2: Search Result Logic (Not Found) ---
    elif row["test_context"] == "detail_search":
        with allure.step(f"Testing Search Logic (Not Found): {row['tc_name']}"):
            home_page.navigate_to_home()

            # The alert appears on the Details page after navigation + fetch
            # We wrap the search action to catch the alert that appears subsequently
            def trigger_search():
                home_page.search_account(row["account_id"])

            alert_text = home_page.alert.get_text_and_accept(trigger_search)
            assert alert_text == row["expected_message"]

    # --- Context 3: Create Account Browser Validation (Tooltips) ---
    elif row["test_context"] == "create_validation":
        with allure.step(f"Testing Create Account Validation: {row['tc_name']}"):
            home_page.navigate_to_home()
            home_page.go_to_create_account()

            # Fill Form Data
            if row["account_holder_name"]: create_page.enter_name(row["account_holder_name"])
            if row["dob"]: create_page.enter_dob(row["dob"])
            if row["gender"]: create_page.select_gender(row["gender"])
            if row["email"]: create_page.enter_email(row["email"])
            if row["phone"]: create_page.enter_phone(row["phone"])
            if row["address"]: create_page.enter_address(row["address"])
            if row["zip_code"]: create_page.enter_zip(row["zip_code"])
            if row["account_type"]: create_page.select_account_type(row["account_type"])
            if row["balance"]: create_page.enter_balance(row["balance"])
            if row["services"]: create_page.select_services(row["services"])
            if row["marketing_opt_in"] == "True": create_page.set_marketing_opt_in("True")
            if row["agreed_to_terms"] == "True": create_page.accept_terms()

            with allure.step("Submit Form and Verify Validation Message"):
                # Trigger Submit
                create_page.click(create_page.SUBMIT_BTN)

                # verify using the Logical Name
                actual_message = create_page.get_validation_message_for_field(row["field_name"])

                assert actual_message == row["expected_message"]