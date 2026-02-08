import os
import pytest
import allure
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from tests.web_selenium.pages.home_page import HomePage
from tests.web_selenium.pages.create_page import CreatePage
from tests.web_selenium.pages.details_page import DetailsPage
from tests.web_selenium.pages.login_page import LoginPage

from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("VITE_BASE_URL")

@pytest.fixture(scope="function")
def driver():
    """Setup Selenium WebDriver (Chrome)"""
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()

    # --- Disable Password Leaks & Manager ---
    prefs = {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
        "profile.password_manager_leak_detection": False,
        # Disabling Safe Browsing is often required to stop the breach popup
        "safebrowsing.enabled": False,
    }
    options.add_experimental_option("prefs", prefs)

    # --- Arguments to suppress popups ---
    # Guest mode natively disables password saving/checking features
    options.add_argument("--guest")

    options.add_argument("--disable-save-password-bubble")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-notifications")

    # Standard stability flags
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")

    options.add_argument("--headless") # Uncomment for headless

    driver = webdriver.Chrome(service=service, options=options)
    driver.maximize_window()
    yield driver
    driver.quit()

@pytest.fixture(scope="session")
def base_url():
    return BASE_URL

# --- Page Objects Fixtures ---
@pytest.fixture
def login_page(driver, base_url):
    hp = LoginPage(driver)
    hp.URL = f"{base_url}/login"
    return hp


@pytest.fixture
def home_page(driver):
    return HomePage(driver)


@pytest.fixture
def create_page(driver):
    return CreatePage(driver)


@pytest.fixture
def details_page(driver):
    return DetailsPage(driver)


# --- Screenshot Hook ---
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        # Check if 'driver' fixture is in the test
        if "driver" in item.funcargs:
            driver = item.funcargs["driver"]
            try:
                allure.attach(
                    driver.get_screenshot_as_png(),
                    name="Failure Screenshot",
                    attachment_type=allure.attachment_type.PNG
                )
            except Exception as e:
                print(f"Failed to capture screenshot: {e}")