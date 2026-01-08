import os
import shutil
import subprocess
import pytest

# Base URL of the application (UI + API)

# Read from env variable, default to localhost for local testing
BASE_URL = os.getenv("BASE_URL", "http://127.0.0.1:9000")


@pytest.fixture(scope="session")
def base_url():
    """
    Exposes BASE_URL as a pytest fixture.
    This allows:
    - dependency injection
    - easy override per environment
    - reuse across UI and API layers
    """
    return BASE_URL


# =========================================================
# Pytest Session Hook – Allure Report Generation
# =========================================================

def pytest_sessionfinish(session, exitstatus):
    """
    Runs once after all tests finish.

    Responsibilities:
    - Preserve Allure history (trend charts)
    - Generate a new Allure HTML report
    """

    # Locate Allure CLI in system PATH
    allure_cmd = shutil.which("allure")
    if not allure_cmd:
        print("\nAllure CLI not found in PATH. Skipping report generation.")
        return

    # Allure directories
    results_dir = "tests/reports/allure-results"   # raw test results
    report_dir = "tests/reports/allure-reports"    # generated HTML report

    # Paths for Allure history (trend data)
    history_src = os.path.join(report_dir, "history")
    history_dest = os.path.join(results_dir, "history")

    # Copy previous history into current results
    # This enables trend charts across test runs
    if os.path.exists(history_src):
        shutil.copytree(history_src, history_dest, dirs_exist_ok=True)

    # Generate Allure report
    subprocess.run(
        [
            allure_cmd,  # Path to the Allure CLI executable (e.g. "allure")
            "generate",  # Allure command → generate a report
            results_dir,  # Input directory: raw allure-results from test run
            "--clean",  # Delete old report data before generating new report
            "-o",  # Output option flag
            report_dir  # Output directory where HTML report will be created
        ],
        check=False  # Do NOT fail pytest even if Allure generation fails
    )

    print("\nAllure report generated with history support.")
