import os
import shutil
import subprocess
import pytest
from tests.api.services.accounts_api import AccountsAPI

BASE_URL = "http://127.0.0.1:9000"


@pytest.fixture(scope="session")
def accounts_api():
    return AccountsAPI(BASE_URL)


def pytest_sessionfinish(session, exitstatus):
    """
    Generate Allure report with history (trend charts)
    """
    allure_cmd = shutil.which("allure")
    if not allure_cmd:
        print("\nAllure CLI not found in PATH. Skipping report generation.")
        return

    results_dir = "tests/api/reports/allure-results"
    report_dir = "tests/api/reports/allure-reports"
    history_src = os.path.join(report_dir, "history")
    history_dest = os.path.join(results_dir, "history")

    # 1️⃣ Copy previous history → allure-results
    if os.path.exists(history_src):
        shutil.copytree(history_src, history_dest, dirs_exist_ok=True)

    # 2️⃣ Generate new report
    subprocess.run(
        [
            allure_cmd,
            "generate",
            results_dir,
            "--clean",
            # "--single-file",
            "-o",
            report_dir
        ],
        check=False
    )

    print("\nAllure report generated with history support.")
