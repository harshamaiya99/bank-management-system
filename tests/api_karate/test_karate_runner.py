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

# Behavior-based Hierarchy
@allure.epic("Bank Management System")
@allure.feature("API Testing - Karate")
@allure.story("End-to-End CRUD - smoke tests")

# Suite-based Hierarchy
@allure.parent_suite("Bank Management System")
@allure.suite("API Testing - Karate")
@allure.sub_suite("End-to-End CRUD - smoke tests")
@pytest.mark.smoke
def test_karate_smoke():
    allure.title("e2e API testing using Karate BDD for accounts/ API - CRUD")
    """
    Triggers only @smoke scenarios in Karate
    """
    run_karate_with_tags("@smoke")


# Behavior-based Hierarchy
@allure.epic("Bank Management System")
@allure.feature("API Testing - Karate")
@allure.story("End-to-End CRUD - regression tests")

# Suite-based Hierarchy
@allure.parent_suite("Bank Management System")
@allure.suite("API Testing - Karate")
@allure.sub_suite("End-to-End CRUD - regression tests")
@pytest.mark.regression
def test_karate_regression():
    allure.title("e2e API testing using Karate BDD for accounts/ API - CRUD")
    """
    Triggers only @regression scenarios in Karate
    """
    run_karate_with_tags("@regression")

# Behavior-based Hierarchy
@allure.epic("Bank Management System")
@allure.feature("API Testing - Karate")
@allure.story("End-to-End CRUD - sit tests")

# Suite-based Hierarchy
@allure.parent_suite("Bank Management System")
@allure.suite("API Testing - Karate")
@allure.sub_suite("End-to-End CRUD - sit tests")
@pytest.mark.sit
def test_karate_sit():
    allure.title("e2e API testing using Karate BDD for accounts/ API - CRUD")
    """
    Triggers only @sit scenarios in Karate
    """
    run_karate_with_tags("@sit")