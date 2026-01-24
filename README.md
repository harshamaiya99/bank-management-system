# Bank Management System & Advanced QA Automation Framework

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat-square&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100.0-009688?style=flat-square&logo=fastapi)
![SQLite](https://img.shields.io/badge/Database-SQLite-003B57?style=flat-square&logo=sqlite)
![Pytest](https://img.shields.io/badge/Tests-Pytest-009688?style=flat-square&logo=pytest)
![Karate](https://img.shields.io/badge/API_Testing-Karate-ED1C24?style=flat-square&logo=karate)
![Playwright](https://img.shields.io/badge/UI_Testing-Playwright-2F80ED?style=flat-square&logo=playwright)
![Selenium](https://img.shields.io/badge/UI_Testing-Selenium-43B02A?style=flat-square&logo=selenium)
![Allure](https://img.shields.io/badge/Reporting-Allure_History-FF7700?style=flat-square&logo=allure)
![GitHub Actions](https://img.shields.io/badge/CI%2FCD-Composite_Actions-2088FF?style=flat-square&logo=github-actions)

## Overview

This project is a full-stack **Bank Management System** designed to demonstrate a robust, production-ready **Test Automation Architecture**.

While the application itself provides a FastAPI backend and a distinct frontend for managing bank accounts, the core value of this repository lies in its **quad-layer testing strategy**. It implements parallel testing frameworks (Selenium vs. Playwright, Pytest vs. Karate) to showcase modern best practices in QA engineering, Design Patterns, and CI/CD pipelines.

---

## Key Enhancements & Features

### 1. Role-Based Access Control (RBAC) & Security
* **JWT Authentication:** Secure login using JWT with Password Flow.
* **User Roles:**
    * **Clerk:** Can View, Create, and Update accounts.
    * **Manager:** Has all Clerk privileges plus **Delete** authority.
* **Security:** Password hashing using `bcrypt`.

### 2. Advanced Design Patterns
* **Service Object Model (SOM):** API tests utilize a service layer (`tests/api_pytest/services/`) to abstract HTTP requests, making tests readable and maintainable.
* **Page Object Model (POM):** Both Playwright and Selenium suites utilize strict POM (`tests/web_*/pages/`) to separate page mechanics from test logic.
* **Singleton Configuration:** Centralized configuration management via `pytest.ini` and `conftest.py`.

### 3. Hybrid Test Frameworks
This project allows you to compare different automation tools side-by-side:
* **API Layer:** Pure Python (`Requests` + `Pytest`) **VS** BDD Style Java/JS (`Karate`).
* **UI Layer:** Modern Async (`Playwright`) **VS** Traditional Synchronous (`Selenium`).

### 4. Intelligent Reporting & CI/CD
* **Allure History:** The CI pipeline automatically preserves test history, generating trend graphs (Pass/Fail ratios over time) hosted on GitHub Pages.
* **Screenshot on Failure:** Automatic capture of full-page screenshots attached to the Allure report whenever a UI test fails.
* **Composite Actions:** GitHub Actions are modularized (Setup, Restore History, Run Tests, Generate Report) for reusability.

---

## Project Structure

```text
.
├── .github                                 # GitHub Actions CI/CD Configuration
│   ├── actions                             # Custom Reusable Composite Actions
│   │   ├── generate-report/action.yml      # Injects metadata & builds Allure HTML
│   │   ├── restore-history/action.yml      # Fetches history for trend graphs
│   │   ├── run-tests/action.yml            # Orchestrates API & UI test execution
│   │   └── setup-env/action.yml            # Installs Python, Java, & Browsers
│   └── workflows
│       └── main.yml                        # Main Pipeline (Triggers on Push/PR)
├── src                                     # Application Source Code
│   ├── backend                             # FastAPI Backend
│   │   ├── auth.py                         # JWT Authentication & Role Logic
│   │   ├── crud.py                         # Database Operations (Create, Read, etc.)
│   │   ├── database.db                     # SQLite Database File
│   │   ├── main.py                         # App Entry Point (Uvicorn)
│   │   ├── models.py                       # Pydantic Schemas & DB Models
│   │   └── routes.py                       # API Endpoints
│   └── frontend                            # Static Web Interface
│       ├── accountDetails.html             # Update/Delete Account Page
│       ├── createAccount.html              # New Account Form
│       ├── home_page.html                  # Dashboard & Search
│       ├── login.html                      # Staff Login Page
│       └── styles.css                      # Global Styling
├── tests                                   # Master Test Suite
│   ├── api_karate                          # BDD API Framework (Karate)
│   │   ├── src/test/java/examples
│   │   │   ├── accounts.feature            # Gherkin Scenarios for API CRUD
│   │   │   ├── auth.feature                # Reusable Auth Helper
│   │   │   ├── karate-config.js            # Global Config (Base URL, Headers)
│   │   │   └── AccountsTest.java           # JUnit Runner
│   │   ├── pom.xml                         # Maven Dependencies
│   │   └── test_karate_runner.py           # Python Wrapper to trigger Karate via Pytest
│   ├── api_pytest                          # Python API Framework (Requests)
│   │   ├── data                            # CSV Test Data
│   │   │   ├── accounts.csv                # Positive Scenarios
│   │   │   └── accounts_negative.csv       # Negative Scenarios (Edge Cases)
│   │   ├── services                        # Service Object Model (SOM)
│   │   │   ├── accounts_api.py             # Accounts Endpoint Wrapper
│   │   │   └── base_api.py                 # Base HTTP Methods (GET, POST, etc.)
│   │   ├── utils                           # API Utilities
│   │   │   ├── allure_logger.py            # Custom Allure Attachments
│   │   │   ├── csv_reader.py               # CSV Parser
│   │   │   ├── expected_response.py        # Response Validation Logic
│   │   │   └── validators.py               # Custom Assertions
│   │   ├── test_accounts_api.py            # Positive Test Suite
│   │   └── test_accounts_api_negative.py   # Negative Test Suite
│   ├── web_playwright                      # Modern UI Framework (Playwright)
│   │   ├── data                            # UI Test Data (CSV)
│   │   ├── pages                           # Page Object Model (POM)
│   │   │   ├── base_page.py                # Core Page Actions
│   │   │   ├── create_page.py              # Create Account Page Objects
│   │   │   ├── details_page.py             # Details Page Objects
│   │   │   ├── home_page.py                # Home Page Objects
│   │   │   └── login_page.py               # Login Page Objects
│   │   ├── utils                           # UI Utilities
│   │   │   ├── alert_handler.py            # Async Alert Listener
│   │   │   ├── assertion_logger.py         # Soft Assertions & Logging
│   │   │   └── csv_reader.py               # Data Provider
│   │   ├── test_e2e_flow.py                # Full CRUD End-to-End Test
│   │   └── test_negative.py                # UI Validation Tests
│   └── web_selenium                        # Traditional UI Framework (Selenium)
│       ├── data                            # Shared UI Test Data
│       ├── pages                           # Selenium Page Objects (POM)
│       ├── utils                           # Selenium Utilities
│       └── test_e2e_flow.py                # Selenium End-to-End Test
├── conftest.py                             # Root Config (Allure History & Hooks)
├── pytest.ini                              # Pytest CLI Configuration
└── requirements.txt                        # Project Dependencies
```


## Getting Started

### Prerequisites
* **Python 3.10+**
* **Java (JDK 11+)** (Required for Allure Report generation and Karate)
* **Node.js & npm** (Required for Playwright)

### Installation

1.  **Clone Repo:**
    ```bash
    git clone <repository-url>
    cd bank-management-system
    ```

2.  **Install Python Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Install Playwright Browsers:**
    ```bash
    playwright install
    ```

4.  **Install Allure Commandline:**
    * Mac: `brew install allure`
    * Windows: `scoop install allure` (or download binary)
    * Linux: `sudo apt-get install allure`

---

## Running the Application

1.  **Start the Server & Initialize database:**
    ```bash
    uvicorn main:app --app-dir src/backend --reload --port 9000
    ```
*   `--port 9000`: Runs the application on port 9000.
*   `--reload`: Enables auto-reloading of the server on code changes during development.

    *Server will start at `http://127.0.0.1:9000`*

2.  **Login Credentials (Seeded on Startup):**

    | Role    | Username  | Password     | Permissions |
    | :---    | :---      | :---         | :--- |
    | Clerk   | `clerk`   | `clerk123`   | Create, Read, Update |
    | Manager | `manager` | `manager123` | Create, Read, Update, **Delete** |

---

### Swagger UI / OpenAPI Documentation

FastAPI automatically generates interactive API documentation. Once the application is running, you can access it at:

*   **Swagger UI**: `http://127.0.0.1:9000/docs`
*   **ReDoc**: `http://127.0.0.1:9000/redoc`

## Frontend Interface

The application includes a minimalist web frontend to demonstrate interaction with the API:

*   **Login Page (`/login.html`)**: Allows logging in using differnt roles and navigating to the "Home" page.
*   **Home Page (`/`)**: Allows searching for accounts by ID and navigating to the "Create Account" page.
*   **Create Account Page (`/createAccount.html`)**: A form to submit new account details. Upon successful creation, an alert displays the new account ID.
*   **Account Details Page (`/accountDetails.html`)**: Displays comprehensive details of an account. It also allows updating existing account information or deleting the account.

## Generating Reports

The project uses `pytest_sessionfinish` hooks to automatically manage report generation.

### Generate & View Report

**Generate HTML report from Allure JSON results:**

``` bash
allure generate tests/reports/allure-results
  -o tests/reports/allure-reports
  --clean
```

**Open the report in your default browser:**

``` bash
allure open tests/reports/allure-reports
```

------------------------------------------------------------------------

## CI/CD Pipeline (GitHub Actions)

The workflow is defined in:

    .github/workflows/main.yml

It runs automatically on every **Push** and **Pull Request**.

### Pipeline Stages

-   **Setup Environment**
    Uses a composite action to install:
    -   Python
    -   JDK (required for Allure)
    -   Playwright browsers
-   **Restore Allure History**
    Downloads previous Allure history from the `allure-history` orphan branch.
    This enables trend analysis such as:
    -   Pass rate changes
    -   Test stability over time
-   **Run Tests**
    Executes:
    -   Backend server
    -   Pytest API tests
    -   Karate BDD tests
    -   Playwright UI tests
    -   Selenium UI tests
-   **Generate Report**
    Injects GitHub metadata into the Allure report, including:
    -   Run ID
    -   Executor information
-   **Publish Report**
    -   Uploads the generated Allure HTML report as a GitHub Actions artifact, allowing it to be downloaded after the workflow completes.
