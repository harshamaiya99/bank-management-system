import pytest

# ---------------- UI Page Object imports ----------------
from tests.web.pages.home_page import HomePage
from tests.web.pages.create_page import CreatePage
from tests.web.pages.details_page import DetailsPage


# =========================================================
# Playwright Configuration Fixture
# =========================================================

@pytest.fixture(scope="session")
def browser_context_args(browser_context_args, base_url):
    """
    Overrides Playwright's internal browser_context_args fixture.

    Purpose:
    - Inject base_url into Playwright
    - Enable page.goto('/path') instead of full URLs
    - Keep UI tests environment-agnostic
    """
    return {
        **browser_context_args,  # keep all default Playwright settings
        "base_url": base_url     # add / override base_url
    }


# =========================================================
# UI Page Object Fixtures (POM)
# =========================================================

@pytest.fixture
def home_page(page):
    """ Provides HomePage object to tests. Page fixture is managed by Playwright. """
    return HomePage(page)


@pytest.fixture
def create_page(page):
    """ Provides CreatePage object to tests. Avoids manual initialization inside tests. """
    return CreatePage(page)


@pytest.fixture
def details_page(page):
    """ Provides DetailsPage object to tests. Keeps test code clean and readable. """
    return DetailsPage(page)