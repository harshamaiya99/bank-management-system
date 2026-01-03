import os
import pytest
from tests.api.utils.csv_reader import read_csv

DATA_FILE = os.path.join(
    os.path.dirname(__file__),
    "data",
    "accounts.csv"
)

test_data = read_csv(DATA_FILE)

@pytest.mark.parametrize("row", test_data, ids=lambda r: r["account_holder_name"])
def test_account_crud_flow(accounts_api, row):

    # ---------- POST ----------
    create_payload = {
        "account_holder_name": row["account_holder_name"],
        "email": row["email"],
        "phone": row["phone"],
        "address": row["address"],
        "account_type": row["account_type"],
        "balance": float(row["balance"]),
        "date_opened": row["date_opened"],
        "status": row["status"]
    }

    create_resp = accounts_api.create_account(create_payload)
    assert create_resp.status_code == 200

    account_id = create_resp.json()["account_id"]
    assert account_id

    # ---------- GET (after POST) ----------
    get_resp = accounts_api.get_account(account_id)
    assert get_resp.status_code == 200
    assert get_resp.json()["email"] == row["email"]

    # ---------- PUT ----------
    update_payload = {
        "account_holder_name": row["updated_account_holder_name"],
        "email": row["updated_email"],
        "phone": row["updated_phone"],
        "address": row["updated_address"],
        "account_type": row["updated_account_type"],
        "balance": float(row["updated_balance"]),
        "date_opened": row["updated_date_opened"],
        "status": row["updated_status"]
    }

    update_resp = accounts_api.update_account(account_id, update_payload)
    assert update_resp.status_code == 200
    assert update_resp.json()["message"] == "Account updated successfully"

    # ---------- GET (after PUT) ----------
    get_updated_resp = accounts_api.get_account(account_id)
    assert get_updated_resp.status_code == 200
    assert get_updated_resp.json()["email"] == row["updated_email"]
    assert get_updated_resp.json()["account_type"] == row["updated_account_type"]

    # ---------- DELETE ----------
    delete_resp = accounts_api.delete_account(account_id)
    assert delete_resp.status_code == 200
    assert delete_resp.json()["message"] == "Account deleted successfully"
