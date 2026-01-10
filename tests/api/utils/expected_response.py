from datetime import date # Import date
class ExpectedResponse:

    @staticmethod
    def expected_response_create_account(account_id, date_opened):
        return {
            "account_id": account_id,
            "date_opened": date_opened,  # Add this expectation
            "message": "Account created successfully"
        }

    @staticmethod
    def expected_response_update_account():
        return {
            "message": "Account updated successfully"
        }

    @staticmethod
    def expected_response_delete_account():
        return {
            "message": "Account deleted successfully"
        }

    @staticmethod
    def expected_response_get_account_create(row, account_id, date_opened):

        return {
            "account_id": account_id,
            "account_holder_name": row["account_holder_name"],
            "dob": row["dob"],
            "gender": row["gender"],
            "email": row["email"],
            "phone": row["phone"],
            "address": row["address"],
            "zip_code": row["zip_code"],
            "account_type": row["account_type"],
            "balance": float(row["balance"]),
            "date_opened": date_opened,
            "status": row["status"],
            "services": row["services"],
            "marketing_opt_in": row["marketing_opt_in"].lower() == "true",
            "agreed_to_terms": True
        }

    @staticmethod
    def expected_response_get_account_update(row, account_id, date_opened):

        return {
            "account_id": account_id,
            "account_holder_name": row["updated_account_holder_name"],
            "dob": row["updated_dob"],
            "gender": row["updated_gender"],
            "email": row["updated_email"],
            "phone": row["updated_phone"],
            "address": row["updated_address"],
            "zip_code": row["updated_zip_code"],
            "account_type": row["updated_account_type"],
            "balance": float(row["updated_balance"]),
            "date_opened": date_opened,
            "status": row["updated_status"],
            "services": row["updated_services"],
            "marketing_opt_in": row["updated_marketing_opt_in"].lower() == "true",
            "agreed_to_terms": True
        }
