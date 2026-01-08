import pytest

# ---------------- API imports ----------------
from tests.api.services.accounts_api import AccountsAPI

# =========================================================
# API Fixtures
# =========================================================

@pytest.fixture(scope="session")
def accounts_api(base_url):
    """
    Creates a single AccountsAPI client for the entire test session.
    Uses dependency injection for base_url instead of hardcoding.
    """
    return AccountsAPI(base_url)