import pytest
import allure
import os
from playwright.sync_api import expect
from tests.web.utils.csv_reader import read_csv_data

TEST_DATA_FILE = os.path.join(os.path.dirname(__file__), "data", "test_data_negative.csv")

@allure.epic("Web UI")
@allure.feature("End to End Banking Flow")
@pytest.mark.parametrize("row", read_csv_data(TEST_DATA_FILE), ids=lambda r: r["tc_name"])
def test_negative_scenarios(home_page, row):
    with allure.step(f"Processing Negative test scenarios:"):
        home_page.navigate_to_home()
        # Enter invalid ID (letters or wrong length)
        home_page.search_account(row["account_id"])
        # Verify the DOM error message
        assert home_page.get_error_message() == "Please enter a valid 7-digit account ID"


