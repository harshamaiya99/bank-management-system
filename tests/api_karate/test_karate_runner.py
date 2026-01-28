import subprocess
import os
import pytest
import allure
from dotenv import load_dotenv

load_dotenv()


def run_karate_with_tags(tags):
    """
    Helper function to run Maven with specific Karate tags.
    """
    test_dir = os.path.dirname(os.path.abspath(__file__))

    # Construct command with tags
    # -Dkarate.options="--tags @yourtag" tells Karate what to run
    command = f"mvn test -B --no-transfer-progress -Dkarate.options=\"--tags {tags}\""

    result = subprocess.run(
        command,
        cwd=test_dir,
        capture_output=True,
        text=True,
        shell=True
    )

    # Attach logs to Allure for debugging
    allure.attach(result.stdout, name="Karate Maven Output", attachment_type=allure.attachment_type.TEXT)

    if result.returncode != 0:
        allure.attach(result.stderr, name="Karate Errors", attachment_type=allure.attachment_type.TEXT)
        pytest.fail(f"Karate tests failed for tags: {tags}")


@allure.epic("API Test - Karate")
@allure.feature("Smoke Tests")
@pytest.mark.smoke
def test_karate_smoke():
    """
    Triggers only @smoke scenarios in Karate
    """
    run_karate_with_tags("@smoke")


@allure.epic("API Test - Karate")
@allure.feature("Regression Tests")
@pytest.mark.regression
def test_karate_regression():
    """
    Triggers only @regression scenarios in Karate
    """
    run_karate_with_tags("@regression")

@allure.epic("API Test - Karate")
@allure.feature("SIT Tests")
@pytest.mark.sit
def test_karate_sit():
    """
    Triggers only @sit scenarios in Karate
    """
    run_karate_with_tags("@sit")