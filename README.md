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
.
├── .github                                 # GitHub Actions CI/CD configuration
│   ├── actions                             # Custom reusable composite actions
│   │   ├── generate-report/action.yml      # Injects metadata and builds Allure HTML report
│   │   ├── restore-history/action.yml      # Fetches history for trend graphs
│   │   ├── run-tests/action.yml            # Orchestrates backend startup and test execution
│   │   └── setup-env/action.yml            # Installs Python, Java, and Playwright browsers
│   └── workflows
│       └── main.yml                        # Main CI/CD pipeline (runs on push/PR)
├── src                                     # Application source code
│   ├── backend                             # FastAPI backend
│   │   ├── accounts                        # Accounts module (logic and routing)
│   │   │   ├── crud.py                     # Database operations (Create, Read, Update, Delete)
│   │   │   ├── router.py                   # API endpoints for accounts
│   │   │   └── schemas.py                  # Pydantic models for data validation
│   │   ├── auth                            # Authentication module
│   │   │   ├── crud.py                     # User lookup logic
│   │   │   ├── router.py                   # Token generation and login endpoints
│   │   │   ├── schemas.py                  # Token and user Pydantic models
│   │   │   └── utils.py                    # JWT creation and password hashing
│   │   ├── database.db                     # SQLite database file
│   │   ├── database.py                     # Database connection and initialization
│   │   ├── main.py                         # FastAPI application entry point
│   │   └── routes_html.py                  # Router for serving frontend HTML files
│   └── frontend                            # Static web interface
│       ├── accountDetails.html             # Page for managing existing accounts
│       ├── createAccount.html              # Form for opening new accounts
│       ├── home_page.html                  # Search dashboard
│       ├── login.html                      # Staff login portal
│       └── styles.css                      # Global styling for the interface
├── tests                                   # Master test suite
│   ├── api_karate                          # BDD API framework (Karate/Java)
│   │   ├── src/test/java/examples
│   │   │   ├── accounts.feature            # Gherkin scenarios for API lifecycle
│   │   │   ├── auth.feature                # Reusable authentication helper
│   │   │   └── AccountsTest.java           # JUnit runner
│   │   ├── karate-config.js                # Global configuration (Base URL, headers)
│   │   ├── pom.xml                         # Maven project configuration
│   │   └── test_karate_runner.py           # Python wrapper to trigger Karate via Pytest
│   ├── api_pytest                          # Python API framework (Requests)
│   │   ├── data                            # CSV test data files
│   │   ├── services                        # Service Object Model (SOM) wrappers
│   │   │   ├── accounts_api.py             # Accounts endpoint logic
│   │   │   └── base_api.py                 # Core HTTP method implementations
│   │   ├── utils                           # API testing utilities
│   │   ├── test_accounts_api.py            # Positive CRUD test scenarios
│   │   └── test_accounts_api_negative.py   # Error handling and validation tests
│   ├── web_playwright                      # Modern UI framework (Playwright)
│   │   ├── data                            # UI test data (CSV)
│   │   ├── pages                           # Page Object Model (POM) classes
│   │   ├── utils                           # UI utilities (Alert handlers, loggers)
│   │   ├── test_e2e_flow.py                # End-to-end user journey tests
│   │   └── test_negative.py                # UI form validation tests
│   └── web_selenium                        # Traditional UI framework (Selenium)
│       ├── data                            # Selenium-specific test data
│       ├── pages                           # Selenium Page Objects
│       ├── utils                           # Standard Selenium utilities
│       └── test_e2e_flow.py                # Selenium end-to-end tests
├── .env.example                            # Template for environment variables
├── .gitignore                              # Git exclusion rules
├── conftest.py                             # Root Pytest config and Allure hooks
├── pytest.ini                              # Pytest command-line configuration
├── README.md                               # Project documentation
└── requirements.txt                        # Project dependencies
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
