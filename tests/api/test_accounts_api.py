import os
import pytest
import allure
from tests.api.utils.csv_reader import read_csv
from tests.api.utils.expected_response import ExpectedResponse

from tests.api.utils.allure_logger import assert_json_match

DATA_FILE = os.path.join(os.path.dirname(__file__), "data", "accounts.csv")

test_data = read_csv(DATA_FILE)


@allure.epic("Accounts API")
@allure.feature("CRUD Operations")
@pytest.mark.parametrize("row", test_data, ids=lambda r: r["account_holder_name"])
def test_account_crud_flow(accounts_api, row):

    with allure.step("Create account (POST)"):
        create_response = accounts_api.create_account(row)
        assert create_response.status_code == 200

        expected_response = ExpectedResponse.expected_response_create_account()
        assert_json_match(create_response.json(), expected_response)

        account_id = create_response.json()["account_id"]

    with allure.step("Get account after creation (GET)"):
        get_response = accounts_api.get_account(account_id)
        assert get_response.status_code == 200

        expected_response = ExpectedResponse.expected_response_get_account_create(row, account_id)
        assert_json_match(get_response.json(), expected_response)

    with allure.step("Update account (PUT)"):
        update_response = accounts_api.update_account(row, account_id)
        assert update_response.status_code == 200

        expected_response = ExpectedResponse.expected_response_update_account()
        assert_json_match(update_response.json(), expected_response)

    with allure.step("Verify updated account (GET)"):
        get_updated_response = accounts_api.get_account(account_id)
        assert get_updated_response.status_code == 200

        expected_response = ExpectedResponse.expected_response_get_account_update(row, account_id)
        assert_json_match(get_updated_response.json(), expected_response)

    with allure.step("Delete account (DELETE)"):
        delete_response = accounts_api.delete_account(account_id)
        assert delete_response.status_code == 200

        expected_response = ExpectedResponse.expected_response_delete_account()
        assert_json_match(delete_response.json(), expected_response)
