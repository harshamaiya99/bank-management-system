# conftest.py
import pytest
from tests.api.services.accounts_api import AccountsAPI

BASE_URL = "http://127.0.0.1:9000"

@pytest.fixture(scope="session")
def accounts_api():
    return AccountsAPI(BASE_URL)
