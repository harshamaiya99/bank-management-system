import os
import shutil
import subprocess


def pytest_sessionfinish(session, exitstatus):
    """
    Runs once after all tests finish.
    1. Preserves Allure history (trend charts).
    2. Generates the new Allure HTML report automatically.
    """

    # 1. Define Paths (Matches your project structure)
    project_root = os.getcwd()
    results_dir = os.path.join(project_root, "tests", "reports", "allure-results")
    report_dir = os.path.join(project_root, "tests", "reports", "allure-report")

    history_src = os.path.join(report_dir, "history")
    history_dst = os.path.join(results_dir, "history")

    # 2. Check for Allure CLI
    allure_cmd = shutil.which("allure")
    if not allure_cmd:
        print("\n[Report] Allure CLI not found in PATH. Skipping report generation.")
        return

    # 3. Preserve History
    # Copy 'history' folder from the previous report to the current results
    if os.path.exists(history_src):
        print(f"\n[History] Preserving trends from: {history_src}")
        # dirs_exist_ok=True allows overwriting if destination exists (Python 3.8+)
        shutil.copytree(history_src, history_dst, dirs_exist_ok=True)
    else:
        print("\n[History] No previous history found. Starting fresh trends.")

    # 4. Generate Report
    print(f"[Report] Generating HTML report to: {report_dir}...")
    try:
        subprocess.run(
            [
                allure_cmd,
                "generate",
                results_dir,
                "--clean",  # Overwrite the old report folder
                "-o",
                report_dir
            ],
            check=True,  # Raise error if generation fails
            shell=True if os.name == 'nt' else False  # Handle Windows path parsing
        )
        print(f"[Report] Success! View it with: allure open {os.path.relpath(report_dir)}")
    except subprocess.CalledProcessError as e:
        print(f"[Report] Failed to generate report. Error: {e}")