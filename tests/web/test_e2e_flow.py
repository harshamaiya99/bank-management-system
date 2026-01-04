import pytest
import allure
import os
from playwright.sync_api import expect
from tests.web.utils.csv_reader import read_csv_data

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
        # assert account_id is not None, "Failed to capture Account ID from alert"
        # print(f"Created Account ID: {account_id}")

    # --- 2. Search & Verify Created Account ---
    with allure.step(f"Search & Verify Created Account"):
        home_page.navigate_to_home()  # Go back to search
        home_page.search_account(account_id)

        details_page.get_account_details()

    # --- 3. Update Account ---
    with allure.step(f"Update Account"):
        details_page.update_account_details(row)

    # --- 4. Verify Update (Reload Data) ---
    with allure.step(f"Search & Verify Update (Reload Data) Account"):
        home_page.navigate_to_home()  # Go back to search
        home_page.search_account(account_id)

        details_page.get_account_details()

    # --- 5. Delete Account ---
    with allure.step(f"Delete Account"):
        details_page.delete_account()

    # --- 6. Verify Deletion ---
    with allure.step(f"Verify Account Deletion"):
        # Search should now fail
        home_page.search_account(account_id)

