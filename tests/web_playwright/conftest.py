import pytest
import allure
import os
from playwright.sync_api import Page
from dotenv import load_dotenv

# Load environment variables (so we can read BASE_URL from .env if it exists)
load_dotenv()

# ---------------- UI Page Object imports ----------------
from tests.web_playwright.pages.home_page import HomePage
from tests.web_playwright.pages.create_page import CreatePage
from tests.web_playwright.pages.details_page import DetailsPage
from tests.web_playwright.pages.login_page import LoginPage

from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("VITE_BASE_URL")

# =========================================================
# Playwright Configuration Fixture
# =========================================================

@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """
    Overrides Playwright's internal browser_context_args fixture.
    """
    return {
        **browser_context_args,
        "base_url": BASE_URL,
        # "viewport": {"width": 1920, "height": 1080},
        # "ignore_https_errors": True
    }


# =========================================================
# UI Page Object Fixtures (POM)
# =========================================================
@pytest.fixture
def login_page(page: Page):
    return LoginPage(page)


@pytest.fixture
def home_page(page: Page):
    return HomePage(page)


@pytest.fixture
def create_page(page: Page):
    return CreatePage(page)


@pytest.fixture
def details_page(page: Page):
    return DetailsPage(page)


# =========================================================
# Hook: Capture Screenshot on Failure
# =========================================================
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Pytest hook to capture a screenshot if a test case fails.
    """
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        if "page" in item.funcargs:
            page = item.funcargs["page"]
            try:
                screenshot_bytes = page.screenshot(full_page=True)
                allure.attach(
                    screenshot_bytes,
                    name=f"Failure Screenshot - {item.name}",
                    attachment_type=allure.attachment_type.PNG
                )
            except Exception as e:
                print(f"Failed to capture screenshot: {e}")