import os
import shutil
import subprocess
import platform
import socket
from datetime import datetime
import pytest


@pytest.fixture(scope="session", autouse=True)
def setup_allure_environment():
    """Create environment information for Allure report"""

    project_root = os.getcwd()
    results_dir = os.path.join(project_root, "tests", "reports", "allure-results")

    # Ensure results directory exists
    os.makedirs(results_dir, exist_ok=True)

    # ------------------------------------------------
    # Collect Environment Information
    # ------------------------------------------------
    environment_data = {
        "OS": platform.system(),
        "OS.Version": platform.version(),
        "Python.Version": platform.python_version(),
        "Hostname": socket.gethostname(),
        "Execution.Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Processor": platform.processor(),
        "Architecture": platform.machine(),

        # Configurable from environment variables
        "Test.Environment": os.getenv("TEST_ENV", "DEV"),
        "Base.URL": os.getenv("BASE_URL", "http://localhost:8000"),
        "Browser": os.getenv("BROWSER", "Chrome"),
        "Database": os.getenv("DATABASE", "SQLite3"),
        "App.Version": os.getenv("APP_VERSION", "3.0.0"),

        # Project Info
        "Project.Name": "Bank Management System",
        "Test.Suite": "API & UI - E2E Tests",
        "CI.Build": os.getenv("BUILD_NUMBER", "Local"),
        "Git.Branch": os.getenv("GIT_BRANCH", "main"),
        "Tester": os.getenv("TESTER_NAME", os.getenv("USERNAME", "Unknown"))
    }

    # ------------------------------------------------
    # Write environment.properties file
    # ------------------------------------------------
    env_file = os.path.join(results_dir, "environment.properties")
    with open(env_file, 'w') as f:
        for key, value in environment_data.items():
            f.write(f"{key}={value}\n")

    print(f"[Allure] Environment information created")

    yield

def pytest_sessionstart(session):
    """Clean results directory BEFORE tests run"""
    project_root = os.getcwd()
    results_dir = os.path.join(project_root, "tests", "reports", "allure-results")

    if os.path.exists(results_dir):
        shutil.rmtree(results_dir)
    os.makedirs(results_dir, exist_ok=True)
    print("[Allure] Results directory cleaned")


def pytest_sessionfinish(session, exitstatus):
    project_root = os.getcwd()
    results_dir = os.path.join(project_root, "tests", "reports", "allure-results")
    report_dir = os.path.join(project_root, "tests", "reports", "allure-report")
    config_file = os.path.join(project_root, "allure.config.json")

    allure_cmd = shutil.which("allure")
    if not allure_cmd:
        print("\n[Allure] CLI not found in PATH.")
        return

    # ------------------------------------------------
    # Clean old report
    # ------------------------------------------------
    if os.path.exists(report_dir):
        shutil.rmtree(report_dir)

    # ------------------------------------------------
    # Generate report
    # ------------------------------------------------
    try:
        subprocess.run(
            [
                allure_cmd,
                "generate",
                results_dir,
                "--config",
                config_file,
                "--history-limit",
                "10"
            ],
            check=True
        )

        print("\n\n[Allure] Report generated successfully.")
        report_index = os.path.join(report_dir, "index.html")
        print(f"[Allure] Open: {report_index}")

    except subprocess.CalledProcessError as e:
        print(f"[Allure] Report generation failed: {e}")