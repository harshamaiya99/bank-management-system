from tests.api.services.base_api import BaseAPI

class AccountsAPI(BaseAPI):

    def create_account(self, payload):
        return self.post("/accounts", payload)

    def get_account(self, account_id):
        return self.get(f"/accounts/{account_id}")

    def update_account(self, account_id, payload):
        return self.put(f"/accounts/{account_id}", payload)

    def delete_account(self, account_id):
        return self.delete(f"/accounts/{account_id}")
