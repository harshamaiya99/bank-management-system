import pytest
from tests.web.pages.home_page import HomePage
from tests.web.pages.create_page import CreatePage
from tests.web.pages.details_page import DetailsPage

# Define Base URL for UI Tests
BASE_URL = "http://127.0.0.1:9000"

@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """Override playwright context to set base url"""
    return {
        **browser_context_args,
        "base_url": BASE_URL
    }

# --- Page Fixtures (So you don't have to init them in every test) ---
@pytest.fixture
def home_page(page):
    return HomePage(page)

@pytest.fixture
def create_page(page):
    return CreatePage(page)

@pytest.fixture
def details_page(page):
    return DetailsPage(page)
