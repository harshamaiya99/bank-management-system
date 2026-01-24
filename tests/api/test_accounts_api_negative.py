import os
import pytest
import allure
from tests.api.utils.csv_reader import read_csv

DATA_FILE = os.path.join(os.path.dirname(__file__), "data", "accounts_negative.csv")
test_data = read_csv(DATA_FILE)


@allure.epic("API Test - Pytest")
@allure.feature("Negative Scenarios")
@pytest.mark.parametrize("row", test_data, ids=lambda r: r["scenario"])
def test_account_negative_scenarios(accounts_api_manager, row):
    """
    Test negative scenarios like Missing Fields.
    Uses 'accounts_api_manager' to authenticate, proving that even valid users
    cannot send invalid data (422 Unprocessable Entity).
    """

    # Alias for readability
    api = accounts_api_manager

    if row["scenario"] == "missing fields":
        with allure.step("Create account with missing fields (POST)"):

            # 1. Construct Payload Dynamically (Partial Data)
            # We cannot use api.create_account() because it expects a full valid row.
            # We must build the dict manually to intentionally omit fields.
            payload = {
                "balance": float(row["balance"]),
                "status": row["status"],
                "agreed_to_terms": True
            }

            optional_fields = [
                "account_holder_name", "dob", "gender", "email",
                "phone", "address", "zip_code", "account_type", "services"
            ]

            missing_fields = []

            for field in optional_fields:
                if row.get(field):
                    payload[field] = row[field]
                else:
                    missing_fields.append(field)

            # Special handling for boolean fields
            if row.get("marketing_opt_in"):
                payload["marketing_opt_in"] = row["marketing_opt_in"].lower() == "true"
            else:
                missing_fields.append("marketing_opt_in")

            print(f"Testing missing fields: {missing_fields}")

            # 2. Construct URL & Headers
            # We manually construct headers here because we are bypassing the helper method
            full_url = f"{api.base_url}/accounts"
            headers = {
                "Content-Type": "application/json",
                "Accept": "application/json",
                "Authorization": f"Bearer {api.token}"
            }

            # 3. Send Request using BaseAPI.post (Handles Allure logging automatically)
            response = api.post(full_url, headers, payload)

            # 4. Assertions
            assert response.status_code == 422, f"Expected 422, got {response.status_code}"

            errors = response.json()["detail"]

            # Verify we got an error for every missing field
            assert len(errors) == len(missing_fields), \
                f"Expected {len(missing_fields)} errors, got {len(errors)}"

            # Verify the error details
            error_locations = [e["loc"][1] for e in errors]
            for missing in missing_fields:
                assert missing in error_locations, f"Field '{missing}' should be in error response"

            for error in errors:
                # Support both Pydantic V1 ('value_error.missing') and V2 ('missing')
                assert error["type"] in ["value_error.missing", "missing"], \
                    f"Unexpected error type: {error['type']}"

                # Support both Pydantic V1 ('field required') and V2 ('Field required')
                assert error["msg"] in ["field required", "Field required"], \
                    f"Unexpected error message: {error['msg']}"

                assert error["loc"][0] == "body"
                assert error["loc"][1] in missing_fields