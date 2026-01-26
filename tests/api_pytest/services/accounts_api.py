import uuid
from tests.api_pytest.services.base_api import BaseAPI

class AccountsAPI(BaseAPI):

    def __init__(self, base_url, token):
        self.base_url = base_url
        self.token = token

    def create_account(self, row):
        url = f'{self.base_url}/accounts'
        headers = {
            "content-type": "application/json",
            "accept": "application/json",
            "Authorization": f"Bearer {self.token}",
            "Idempotency-Id": str(uuid.uuid4()),
            "X-Process-Id": str(uuid.uuid4())
        }

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
            "status": row["status"],
            "services": row["services"],  # Stores comma-separated values (e.g., "SMS,DebitCard")
            "marketing_opt_in": row["marketing_opt_in"].lower() == "true",
            "agreed_to_terms": True
        }
        return self.post(url, headers, create_payload)

    def get_account(self, account_id):
        url = f'{self.base_url}/accounts/{account_id}'
        headers = {
            "content-type": "application/json",
            "accept": "application/json",
            "Authorization": f"Bearer {self.token}",
            "X-Process-Id": str(uuid.uuid4())
        }

        return self.get(url, headers)

    def update_account(self, row, account_id):
        url = f'{self.base_url}/accounts/{account_id}'
        headers = {
            "content-type": "application/json",
            "accept": "application/json",
            "Authorization": f"Bearer {self.token}",
            "X-Process-Id": str(uuid.uuid4())
        }

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
            "status": row["updated_status"],
            "services": row["updated_services"],
            "marketing_opt_in": row["updated_marketing_opt_in"].lower() == "true",
            "agreed_to_terms": True
        }

        return self.put(url, headers, update_payload)

    def delete_account(self, account_id):
        url = f'{self.base_url}/accounts/{account_id}'
        headers = {
            "content-type": "application/json",
            "accept": "application/json",
            "Authorization": f"Bearer {self.token}",
            "X-Process-Id": str(uuid.uuid4())
        }
        return self.delete(url, headers)
