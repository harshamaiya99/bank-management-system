import subprocess
import os
import pytest

def test_execute_karate_tests():
    """
    Wrapper test that executes 'mvn test' for Karate.
    This allows Pytest to trigger the Java-based Karate tests.
    """
    # 1. Determine the directory where this script (and pom.xml) is located
    test_dir = os.path.dirname(os.path.abspath(__file__))

    # 2. Run the Maven command
    #    cwd=test_dir ensures we run it from 'tests/api_karate/' folder
    result = subprocess.run(
        "mvn test",
        cwd=test_dir,
        capture_output=True,
        text=True,
        shell=True  # Required for Windows (PS/CMD) usually
    )

    # 3. Print the output so you can see it in pytest (use -s to view)
    print("\n" + "="*40)
    print("KARATE MAVEN OUTPUT")
    print("="*40)
    print(result.stdout)
    if result.stderr:
        print("ERRORS:")
        print(result.stderr)
    print("="*40)

    # 4. Fail the Pytest if Maven failed (non-zero exit code)
    assert result.returncode == 0, "Karate Tests Failed! See output above."