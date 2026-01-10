from tests.api.services.base_api import BaseAPI

class AccountsAPI(BaseAPI):

    def create_account(self, row):
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
            "marketing_opt_in": row["marketing_opt_in"].lower() == "true",
            "agreed_to_terms": True
        }
        return self.post("/accounts", create_payload)

    def get_account(self, account_id):
        return self.get(f"/accounts/{account_id}")

    def update_account(self, row, account_id):
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
            "marketing_opt_in": row["updated_marketing_opt_in"].lower() == "true",
            "agreed_to_terms": True
        }

        return self.put(f"/accounts/{account_id}", update_payload)

    def delete_account(self, account_id):
        return self.delete(f"/accounts/{account_id}")
