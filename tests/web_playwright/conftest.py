import pytest
import allure
from playwright.sync_api import Page

# ---------------- UI Page Object imports ----------------
from tests.web_playwright.pages.home_page import HomePage
from tests.web_playwright.pages.create_page import CreatePage
from tests.web_playwright.pages.details_page import DetailsPage


# =========================================================
# Playwright Configuration Fixture
# =========================================================

@pytest.fixture(scope="session")
def browser_context_args(browser_context_args, base_url):
    """
    Overrides Playwright's internal browser_context_args fixture.
    """
    return {
        **browser_context_args,
        "base_url": base_url
    }


# =========================================================
# UI Page Object Fixtures (POM)
# =========================================================

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
# This decorator ensures the hook runs at the correct time to inspect the test outcome.
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Pytest hook to capture a screenshot if a test case fails.
    It checks if the 'page' fixture is present (indicating a UI test).
    """
    # Execute all other hooks to obtain the report object
    outcome = yield # This yields control to execute the test
    report = outcome.get_result() # retrieves the test report (pass/fail status).

    # We only care about the "call" phase (actual test execution) and if it failed
    if report.when == "call" and report.failed:

        # Check if the test used the 'page' fixture (Playwright)
        if "page" in item.funcargs:
            page = item.funcargs["page"] # dynamically retrieve the page fixture instance used in the failed test to take the screenshot.

            try:
                # Capture screenshot as bytes
                screenshot_bytes = page.screenshot(full_page=True)

                # Attach to Allure Report
                allure.attach(
                    screenshot_bytes,
                    name=f"Failure Screenshot - {item.name}",
                    attachment_type=allure.attachment_type.PNG
                )
            except Exception as e:
                print(f"Failed to capture screenshot: {e}")