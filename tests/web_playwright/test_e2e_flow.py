import pytest
import allure
import os
from dotenv import load_dotenv
from tests.web_playwright.utils.get_data_with_markers import get_data_with_markers
from tests.web_playwright.utils.assertion_logger import assert_ui_match, assert_message_match, assert_toast_match

load_dotenv()
TEST_DATA_FILE = os.path.join(os.path.dirname(__file__), "data", "test_data.csv")
test_data = get_data_with_markers(TEST_DATA_FILE)


@allure.epic("Web UI Test - Playwright")
@allure.feature("End-to-End test flow")
@pytest.mark.parametrize("row", test_data, ids=lambda r: r["account_holder_name"])
def test_end_to_end_crud(login_page, home_page, create_page, details_page, row):
    # --- 1. Navigate & Create ---
    with allure.step(f"Login Page"):
        login_page.navigate_to_login()
        manager_user = os.getenv("MANAGER_USERNAME")
        manager_pass = os.getenv("MANAGER_PASSWORD")
        login_page.login(manager_user, manager_pass)

    with allure.step(f"Create Account"):
        home_page.go_to_create_account()

        # Unpack tuple: ID, Title, Description
        account_id, toast_title, toast_desc = create_page.create_new_account(row)

        # Build Expected Description dynamically
        # Matches logic in CreateAccountPage.tsx: `Successfully created account ${data.account_id} for ${variables.account_holder_name}`
        expected_desc_pattern = f"Successfully created account \\d{{7}} for {row['account_holder_name']}"

        # Use new assertion helper
        assert_toast_match(
            actual_title=toast_title,
            actual_desc=toast_desc,
            expected_title="Account Opened",
            expected_desc_pattern=expected_desc_pattern,
            is_regex=True
        )

    # --- 2. Search & Verify Created Account ---
    with allure.step(f"Search & Verify Created Account"):
        # Note: If the app redirects to details automatically (which it does),
        # we might already be there. But searching again validates the ID lookup flow.
        home_page.navigate_to_dashboard()  # Go back to dashboard to test search
        home_page.search_account(account_id)

        actual_data = details_page.get_account_details_as_dict()

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
            "status": "Active",
            "services": row["services"],
            "marketing_opt_in": row["marketing_opt_in"].lower()
        }
        assert_ui_match(actual_data, expected_data)

    # --- 3. Update Account ---
    with allure.step(f"Update Account"):
        toast_title, toast_desc = details_page.update_account_details(row)
        assert_toast_match(
            actual_title=toast_title,
            actual_desc=toast_desc,
            expected_title="Changes Saved",
            expected_desc_pattern="Account details have been successfully updated."
        )

    # --- 4. Verify Update ---
    with allure.step(f"Search & Verify Update"):
        # home_page.navigate_to_dashboard()  # Go back to dashboard to test search
        # home_page.search_account(account_id)

        actual_updated_data = details_page.get_account_details_as_dict()

        expected_updated_data = {
            "account_id": account_id,
            "account_holder_name": row["updated_account_holder_name"],
            "dob": row["updated_dob"],
            "gender": row["updated_gender"],
            "email": row["updated_email"],
            "phone": row["updated_phone"],
            "address": row["updated_address"],
            "zip_code": row["updated_zip_code"],
            # Account Type is disabled/immutable, so it should match original
            "account_type": row["account_type"],
            "balance": row["updated_balance"],
            "status": row["updated_status"],
            "services": row["updated_services"],
            "marketing_opt_in": row["updated_marketing_opt_in"].lower()
        }
        assert_ui_match(actual_updated_data, expected_updated_data)

    # --- 5. Delete Account ---
    with allure.step(f"Delete Account"):
        toast_title, toast_desc = details_page.delete_account()
        assert_toast_match(
            actual_title=toast_title,
            actual_desc=toast_desc,
            expected_title="Account Deleted",
            expected_desc_pattern=f"Account {account_id} has been permanently removed."
        )

    # --- 6. Verify Deletion ---
    with allure.step(f"Verify Account Deletion"):
        home_page.search_account(account_id)
        not_found_msg = home_page.get_error_message()
        assert_message_match(not_found_msg, "Account not found.", context="Deleted Account Search")

    with allure.step(f"Logout"):
        home_page.logout()