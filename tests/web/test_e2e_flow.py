import pytest
import allure
import os
from playwright.sync_api import expect
from tests.web.utils.csv_reader import read_csv_data
from tests.web.utils.assertion_logger import assert_ui_match

TEST_DATA_FILE = os.path.join(os.path.dirname(__file__), "data", "test_data.csv")

@allure.epic("Web UI")
@allure.feature("End to End Banking Flow")
@pytest.mark.parametrize("row", read_csv_data(TEST_DATA_FILE), ids=lambda r: r["account_holder_name"])
def test_end_to_end_crud(home_page, create_page, details_page, row):
    """
    Executes a full lifecycle test for each user in the CSV:
    Create -> Search -> Verify -> Update -> Search -> Verify -> Delete -> Search -> Confirm Not Found
    """
    # --- 1. Navigate & Create ---
    with allure.step(f"Processing E2E Test for: {row['account_holder_name']}"):
        home_page.navigate_to_home()

    with allure.step(f"Create Account"):
        home_page.go_to_create_account()

        account_id = create_page.create_new_account(row)

    # --- 2. Search & Verify Created Account ---
    with allure.step(f"Search & Verify Created Account"):
        home_page.search_account(account_id)

        # A. Capture Actual State from UI
        actual_data = details_page.get_account_details_as_dict()

        # B. Build Expected State
        expected_data = {
            "account_id": account_id,
            "account_holder_name": row["account_holder_name"],
            "dob": row["dob"],
            "gender": row["gender"],
            "email": row["email"],
            "phone": row["phone"],
            "address": row["address"],
            "zip_code": row["zip_code"],
            "account_type": row["account_type"],
            "balance": row["balance"],
            "status": "Active",  # <--- Default status on creation is Active
            "services": row["services"],
            "marketing_opt_in": row["marketing_opt_in"].lower()
        }

        # C. Perform Standardized Assertion
        assert_ui_match(actual_data, expected_data)

    # --- 3. Update Account ---
    with allure.step(f"Update Account"):
        details_page.update_account_details(row)

    # --- 4. Verify Update (Reload Data) ---
    with allure.step(f"Search & Verify Update (Reload Data) Account"):
        home_page.search_account(account_id)

        # A. Capture Actual Updated State
        actual_updated_data = details_page.get_account_details_as_dict()

        # B. Build Expected Updated State
        expected_updated_data = {
            "account_id": account_id,
            "account_holder_name": row["updated_account_holder_name"],
            "dob": row["updated_dob"],
            "gender": row["updated_gender"],
            "email": row["updated_email"],
            "phone": row["updated_phone"],
            "address": row["updated_address"],
            "zip_code": row["updated_zip_code"],
            "account_type": row["updated_account_type"],
            "balance": row["updated_balance"],
            "status": row["updated_status"],
            "services": row["updated_services"],
            "marketing_opt_in": row["updated_marketing_opt_in"].lower()
        }

        # C. Perform Standardized Assertion
        assert_ui_match(actual_updated_data, expected_updated_data)

    # --- 5. Delete Account ---
    with allure.step(f"Delete Account"):
        details_page.delete_account()

    # --- 6. Verify Deletion ---
    with allure.step(f"Verify Account Deletion"):
        # Search should now fail
        home_page.search_account(account_id)


