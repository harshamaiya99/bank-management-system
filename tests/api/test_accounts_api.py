import os
import pytest
import allure
from tests.api.utils.csv_reader import read_csv

DATA_FILE = os.path.join(os.path.dirname(__file__), "data", "accounts.csv")

test_data = read_csv(DATA_FILE)

@allure.epic("Accounts API")
@allure.feature("CRUD Operations")
@pytest.mark.parametrize("row", test_data, ids=lambda r: r["account_holder_name"])
def test_account_crud_flow(accounts_api, row):

    with allure.step("Create account (POST)"):
        create_payload = {
            "account_holder_name": row["account_holder_name"],
            "dob": row["dob"],
            "gender": row["gender"],
            "email": row["email"],
            "phone": row["phone"],
            "address": row["address"],
            "zip_code": row["zip_code"],
            "account_type": row["account_type"],
            "balance": float(row["balance"]),
            "date_opened": row["date_opened"],
            "status": row["status"],
            "services": row["services"],  # Stores comma-separated values (e.g., "SMS,DebitCard")
            "marketing_opt_in": bool(row["marketing_opt_in"]),
            "agreed_to_terms": True
        }

        create_resp = accounts_api.create_account(create_payload)
        assert create_resp.status_code == 200
        assert create_resp.json()["message"] == "Account created successfully"

        account_id = create_resp.json()["account_id"]

    with allure.step("Get account after creation (GET)"):
        get_resp = accounts_api.get_account(account_id)
        assert get_resp.status_code == 200
        assert get_resp.json()["account_id"] == account_id
        assert get_resp.json()["account_holder_name"] == row["account_holder_name"]
        assert get_resp.json()["dob"] == row["dob"]
        assert get_resp.json()["gender"] == row["gender"]
        assert get_resp.json()["email"] == row["email"]
        assert get_resp.json()["phone"] == row["phone"]
        assert get_resp.json()["address"] == row["address"]
        assert get_resp.json()["zip_code"] == row["zip_code"]
        assert get_resp.json()["account_type"] == row["account_type"]
        assert get_resp.json()["balance"] == float(row["balance"])
        assert get_resp.json()["date_opened"] == row["date_opened"]
        assert get_resp.json()["status"] == row["status"]
        assert get_resp.json()["services"] == row["services"]
        assert get_resp.json()["marketing_opt_in"] == bool(row["marketing_opt_in"])
        assert get_resp.json()["agreed_to_terms"] == True

    with allure.step("Update account (PUT)"):
        update_payload = {
            "account_holder_name": row["updated_account_holder_name"],
            "dob": row["updated_dob"],
            "gender": row["updated_gender"],
            "email": row["updated_email"],
            "phone": row["updated_phone"],
            "address": row["updated_address"],
            "zip_code": row["updated_zip_code"],
            "account_type": row["updated_account_type"],
            "balance": float(row["updated_balance"]),
            "date_opened": row["updated_date_opened"],
            "status": row["updated_status"],
            "services": row["updated_services"],
            "marketing_opt_in": bool(row["updated_marketing_opt_in"]),
            "agreed_to_terms": True
        }

        update_resp = accounts_api.update_account(account_id, update_payload)
        assert update_resp.status_code == 200
        assert update_resp.json()["message"] == "Account updated successfully"

    with allure.step("Verify updated account (GET)"):
        get_updated_resp = accounts_api.get_account(account_id)
        assert get_updated_resp.status_code == 200
        assert get_updated_resp.json()["account_id"] == account_id
        assert get_updated_resp.json()["account_holder_name"] == row["updated_account_holder_name"]
        assert get_updated_resp.json()["dob"] == row["updated_dob"]
        assert get_updated_resp.json()["gender"] == row["updated_gender"]
        assert get_updated_resp.json()["email"] == row["updated_email"]
        assert get_updated_resp.json()["phone"] == row["updated_phone"]
        assert get_updated_resp.json()["address"] == row["updated_address"]
        assert get_updated_resp.json()["zip_code"] == row["updated_zip_code"]
        assert get_updated_resp.json()["account_type"] == row["updated_account_type"]
        assert get_updated_resp.json()["balance"] == float(row["updated_balance"])
        assert get_updated_resp.json()["date_opened"] == row["updated_date_opened"]
        assert get_updated_resp.json()["status"] == row["updated_status"]
        assert get_updated_resp.json()["services"] == row["updated_services"]
        assert get_updated_resp.json()["marketing_opt_in"] == bool(row["updated_marketing_opt_in"])
        assert get_updated_resp.json()["agreed_to_terms"] == True

    with allure.step("Delete account (DELETE)"):
        delete_resp = accounts_api.delete_account(account_id)
        assert delete_resp.status_code == 200
        assert delete_resp.json()["message"] == "Account deleted successfully"
