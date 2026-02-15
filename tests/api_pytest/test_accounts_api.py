import os
import pytest
import allure

from tests.api_pytest.utils.get_data_with_markers import get_data_with_markers
from tests.api_pytest.utils.expected_response import ExpectedResponse
from tests.api_pytest.utils.allure_logger import assert_json_match

TEST_DATA_FILE = os.path.join(os.path.dirname(__file__), "data", "accounts.csv")

# Load the processed data
test_data = get_data_with_markers(TEST_DATA_FILE)

# Behavior-based Hierarchy
@allure.epic("Bank Management System")
@allure.feature("API Testing - Pytest")
@allure.story("End-to-End CRUD")

# Suite-based Hierarchy
@allure.parent_suite("Bank Management System")
@allure.suite("API Testing - Pytest")
@allure.sub_suite("End-to-End CRUD")

@pytest.mark.parametrize("row", test_data)
def test_account_crud_flow(accounts_api_manager, row):
    allure.dynamic.title(f"{row['tc_no']} {row['tc_name']}")

    with allure.step("Create account (POST)"):
        create_response = accounts_api_manager.create_account(row)
        assert create_response.status_code == 200

        expected_response = ExpectedResponse.expected_response_create_account()
        assert_json_match(create_response.json(), expected_response)

        account_id = create_response.json()["account_id"]

    with allure.step("Get account after creation (GET)"):
        get_response = accounts_api_manager.get_account(account_id)
        assert get_response.status_code == 200

        expected_response = ExpectedResponse.expected_response_get_account_create(row, account_id)
        assert_json_match(get_response.json(), expected_response)

    with allure.step("Update account (PUT)"):
        update_response = accounts_api_manager.update_account(row, account_id)
        assert update_response.status_code == 200

        expected_response = ExpectedResponse.expected_response_update_account()
        assert_json_match(update_response.json(), expected_response)

    with allure.step("Verify updated account (GET)"):
        get_updated_response = accounts_api_manager.get_account(account_id)
        assert get_updated_response.status_code == 200

        expected_response = ExpectedResponse.expected_response_get_account_update(row, account_id)
        assert_json_match(get_updated_response.json(), expected_response)

    with allure.step("Delete account (DELETE)"):
        delete_response = accounts_api_manager.delete_account(account_id)
        assert delete_response.status_code == 200

        expected_response = ExpectedResponse.expected_response_delete_account()
        assert_json_match(delete_response.json(), expected_response)
