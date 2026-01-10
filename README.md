# Bank Account Management Application

![Python](https://img.shields.io/badge/Python-3.9+-blue?style=flat-square&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100.0-009688?style=flat-square&logo=fastapi)
![SQLite](https://img.shields.io/badge/Database-SQLite-003B57?style=flat-square&logo=sqlite)
![Pytest](https://img.shields.io/badge/Tests-Pytest-009688?style=flat-square&logo=pytest)
![Allure Report](https://img.shields.io/badge/Reporting-Allure-FF7700?style=flat-square&logo=allure)
![Playwright](https://img.shields.io/badge/UI_Testing-Playwright-2F80ED?style=flat-square&logo=playwright)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

## Table of Contents

*   [Overview](#overview)
*   [Features](#features)
*   [Technologies Used](#technologies-used)
*   [Project Structure](#project-structure)
*   [Getting Started](#getting-started)
    *   [Prerequisites](#prerequisites)
    *   [Installation](#installation)
    *   [Database Initialization](#database-initialization)
    *   [Running the Application](#running-the-application)
*   [API Endpoints](#api-endpoints)
    *   [Swagger UI / OpenAPI Documentation](#swagger-ui--openapi-documentation)
*   [Frontend Interface](#frontend-interface)
*   [Database Management](#database-management)
*   [Testing](#testing)
    *   [API Testing](#api-testing)
    *   [Web UI Testing (Playwright)](#web-ui-testing-playwright)
    *   [Generating Allure Report](#generating-allure-report)
    *   [Viewing Allure Report](#viewing-allure-report)
*   [Contributing](#contributing)
*   [License](#license)
*   [Acknowledgements](#acknowledgements)

---

## Overview

This project implements a comprehensive **Bank Account Management API** using **FastAPI** as the backend framework and **SQLite** for data persistence. It provides a robust set of RESTful endpoints for managing bank accounts, including creation, retrieval, updates, and deletion.

Accompanying the API is a simple web-based user interface (frontend) built with pure HTML, CSS, and JavaScript, served directly by FastAPI using Jinja2 templates. The project also features extensive automated testing, covering both API integration tests with `requests` and `pytest`, and end-to-end web UI tests using `Playwright`. Test results are meticulously captured and presented through **Allure Reports**, offering detailed insights into test execution, failures, and historical trends.

## Features

*   **Account CRUD Operations:** Full Create, Read, Update, and Delete functionality for bank accounts.
*   **FastAPI Backend:** High-performance, easy-to-use API development with automatic OpenAPI documentation.
*   **SQLite Database:** Lightweight and serverless database for local data storage.
*   **Simple Web UI:** Basic HTML/CSS/JS interface for interacting with the API (creating, searching, viewing, updating, deleting accounts).
*   **CORS Enabled:** Configured to allow cross-origin requests for flexible client-side integration.
*   **Health Check Endpoint:** `/health` endpoint for monitoring API status.
*   **Comprehensive Testing:**
    *   **API Tests:** Pytest-based tests verifying core API logic using `requests` and data-driven testing from CSV files.
    *   **Web UI (E2E) Tests:** Playwright-based tests simulating user interactions in a real browser, covering full lifecycle scenarios and negative cases.
*   **Allure Reporting:** Automated generation of rich, interactive test reports with detailed steps, request/response payloads, and history.

## Technologies Used

*   **Python 3.9+**: The core programming language for both backend and testing.
*   **FastAPI**: Modern, fast (high-performance) web framework for building APIs with Python 3.7+ based on standard Python type hints.
*   **Uvicorn**: An ASGI server for running FastAPI applications.
*   **SQLite**: A C-language library that implements a small, fast, self-contained, high-reliability, full-featured, SQL database engine.
*   **Pydantic**: Data validation and settings management using Python type hints, integral to FastAPI's request/response models.
*   **Jinja2**: A modern and designer-friendly templating language for Python, used for rendering HTML pages.
*   **Pytest**: A mature full-featured Python testing framework.
*   **Requests**: An elegant and simple HTTP library for Python, used in API tests.
*   **Playwright**: A Python library to automate Chromium, Firefox and WebKit with a single API, used for robust end-to-end web UI testing.
*   **Allure Report**: A flexible lightweight multi-language test report tool that gives a clear overview of the test execution, including trends and detailed steps.

## Project Structure

```
.
├── src/
│   ├── backend/
│   │   ├── __init__.py
│   │   ├── crud.py            # Database Create, Read, Update, Delete (CRUD) operations
│   │   ├── database.py        # SQLite database connection and initialization
│   │   ├── main.py            # FastAPI application entry point, CORS, router inclusion
│   │   ├── models.py          # Pydantic models for API request/response
│   │   └── routes.py          # API endpoints and HTML template rendering
│   └── frontend/
│       ├── accountDetails.html # HTML page for viewing/updating account details
│       ├── createAccount.html  # HTML page for creating new accounts
│       └── index.html          # Home page with search and create options
├── tests/
│   ├── api/
│   │   ├── data/
│   │   │   └── accounts.csv   # Test data for API CRUD operations
│   │   ├── services/
│   │   │   ├── accounts_api.py # API client for accounts endpoints
│   │   │   └── base_api.py     # Base API client with common request logic and Allure logging
│   │   ├── utils/
│   │   │   ├── allure_logger.py # Utility for attaching request/response to Allure
│   │   │   └── csv_reader.py    # Utility to read CSV test data
│   │   └── test_accounts_api.py # Pytest tests for API CRUD operations
│   ├── web/
│   │   ├── data/
│   │   │   ├── test_data.csv        # Test data for positive E2E UI flow
│   │   │   └── test_data_negative.csv # Test data for negative UI scenarios
│   │   ├── pages/                   # Playwright Page Object Model
│   │   │   ├── __init__.py
│   │   │   ├── base_page.py         # Base page class with common Playwright actions
│   │   │   ├── create_page.py       # Page object for Create Account form
│   │   │   ├── details_page.py      # Page object for Account Details page
│   │   │   └── home_page.py         # Page object for Home page
│   │   ├── utils/
│   │   │   ├── __init__.py
│   │   │   ├── alert_handler.py     # Utility to handle Playwright dialogs/alerts
│   │   │   └── csv_reader.py        # Utility to read CSV test data for UI tests
│   │   ├── conftest.py              # Playwright fixtures and page object initializations
│   │   ├── test_e2e_flow.py         # Playwright end-to-end UI tests
│   │   └── test_negative.py         # Playwright negative UI tests
│   ├── conftest.py                  # Global pytest fixtures, including Allure report generation hook
│   └── reports/                     # Directory for Allure test results and generated reports
│       └── allure-results/          # Raw Allure test results
│       └── allure-reports/          # Generated HTML Allure report
├── .pytest_cache/                 # Pytest cache directory (should be ignored by Git)
├── requirements.txt               # Project dependencies
└── README.md                      # Project documentation
```

## Getting Started

Follow these steps to set up and run the Bank Account Management API locally.

### Prerequisites

*   **Python 3.9+**
*   **pip** (Python package installer)
*   **Node.js & npm** (required by Playwright to install browser binaries)

### Installation

1.  **Clone the repository (if applicable):**

    ```bash
    git clone <repository-url>
    cd web-FastAPI-SQLlite
    ```

2.  **Create and activate a virtual environment:**

    ```bash
    python -m venv venv
    # On Windows:
    .\venv\Scripts\activate
    # On macOS/Linux:
    source venv/bin/activate
    ```

3.  **Install project dependencies:**

    Create a `requirements.txt` file in the root of your project with the following content:

    ```
    fastapi==0.100.0
    uvicorn[standard]
    pydantic
    Jinja2
    pytest
    requests
    allure-pytest
    playwright
    ```

    Then install:

    ```bash
    pip install -r requirements.txt
    ```

4.  **Install Playwright browser binaries:**

    ```bash
    playwright install
    ```

### Database Initialization

The project uses SQLite, and the database schema is automatically created if it doesn't exist when `database.py` is run.

```bash
python src/backend/database.py
```
This will create a `database.db` file within the `src/backend/` directory if it doesn't already exist, and set up the necessary `accounts` table.

### Running the Application

To start the FastAPI application:

```bash
uvicorn src.backend.main:app --host 0.0.0.0 --port 9000 --reload
```

*   `--host 0.0.0.0`: Makes the server accessible from other machines on the network (useful for Docker or external testing).
*   `--port 9000`: Runs the application on port 9000.
*   `--reload`: Enables auto-reloading of the server on code changes during development.

The API will be accessible at `http://127.0.0.1:9000`.

## API Endpoints

The API provides the following endpoints for managing bank accounts:

| Method | Endpoint                    | Description                                  | Request Body (Example)                                     | Response Body (Example)                                     |
| :----- | :-------------------------- | :------------------------------------------- | :--------------------------------------------------------- | :---------------------------------------------------------- |
| `GET`  | `/health`                   | Checks the health status of the API.         | `N/A`                                                      | `{"status": "healthy"}`                                     |
| `GET`  | `/`                         | Serves the main HTML home page.              | `N/A`                                                      | HTML content                                                |
| `GET`  | `/createAccount.html`       | Serves the HTML page for creating accounts.  | `N/A`                                                      | HTML content                                                |
| `GET`  | `/accountDetails.html`      | Serves the HTML page for account details.    | `N/A`                                                      | HTML content                                                |
| `GET`  | `/accounts`                 | Retrieves a list of all bank accounts.       | `N/A`                                                      | `[{"account_id": "...", "account_holder_name": "...", ...}]` |
| `POST` | `/accounts`                 | Creates a new bank account.                  | `AccountCreate` model (see below)                          | `{"account_id": "...", "message": "Account created successfully"}` |
| `GET`  | `/accounts/{account_id}`    | Retrieves details for a specific account.    | `N/A`                                                      | `AccountResponse` model (see below) or `404`                |
| `PUT`  | `/accounts/{account_id}`    | Updates details for a specific account.      | `AccountUpdate` model (see below)                          | `{"message": "Account updated successfully"}`               |
| `DELETE` | `/accounts/{account_id}`  | Deletes a specific account.                  | `N/A`                                                      | `{"message": "Account deleted successfully"}`               |

### Swagger UI / OpenAPI Documentation

FastAPI automatically generates interactive API documentation. Once the application is running, you can access it at:

*   **Swagger UI**: `http://127.0.0.1:9000/docs`
*   **ReDoc**: `http://127.0.0.1:9000/redoc`

## Frontend Interface

The application includes a minimalist web frontend to demonstrate interaction with the API:

*   **Home Page (`/`)**: Allows searching for accounts by ID and navigating to the "Create Account" page.
*   **Create Account Page (`/createAccount.html`)**: A form to submit new account details. Upon successful creation, an alert displays the new account ID.
*   **Account Details Page (`/accountDetails.html`)**: Displays comprehensive details of an account. It also allows updating existing account information or deleting the account.

## Database Management

The SQLite database file `database.db` is located in `src/backend/`. You can use any SQLite browser (e.g., [DB Browser for SQLite](https://sqlitebrowser.org/)) to inspect the database schema and data directly.

## Testing

The project is equipped with both API and Web UI tests, and uses Allure for comprehensive reporting.

### API Testing

API tests are located in `tests/api/`. They use `pytest` and the `requests` library to perform CRUD operations against the running API. Test data is driven by `tests/api/data/accounts.csv`.

To run API tests:

```bash
pytest tests/api/ --alluredir=tests/reports/allure-results
```

### Web UI Testing (Playwright)

Web UI end-to-end tests are located in `tests/web/`. They use `pytest` and `Playwright` to simulate user interactions in a browser (Chromium by default). Test data for positive scenarios is in `tests/web/data/test_data.csv`, and for negative scenarios in `tests/web/data/test_data_negative.csv`.

To run Web UI tests:

```bash
pytest tests/web/ --alluredir=tests/reports/allure-results
```

You can specify a browser (e.g., `firefox`, `webkit`) using `--browser`:

```bash
pytest tests/web/ --browser=firefox --alluredir=tests/reports/allure-results
```

### Generating Allure Report

After running your tests (API or Web UI), raw Allure results will be generated in `tests/reports/allure-results`. To generate the human-readable HTML report:

```bash
allure generate tests/reports/allure-results -o tests/reports/allure-reports --clean
```

The `--clean` flag will clean the previous report data before generating a new one, ensuring fresh results. The `conftest.py` in the root also handles copying history and generating the report automatically upon `pytest_sessionfinish`.

### Viewing Allure Report

To open the generated Allure Report in your default web browser:

```bash
allure open tests/reports/allure-reports
```

This will launch a local web server to host the report, allowing you to browse test results, statistics, and trends.

## Contributing

Contributions are welcome! Please follow these steps:

1.  Fork the repository.
2.  Create a new branch (`git checkout -b feature/your-feature-name`).
3.  Make your changes and ensure tests pass.
4.  Commit your changes (`git commit -m 'Add new feature'`).
5.  Push to the branch (`git push origin feature/your-feature-name`).
6.  Open a Pull Request.

## License

This project is licensed under the MIT License - see the `LICENSE` file for details.

## Acknowledgements

*   [FastAPI](https://fastapi.tiangolo.com/)
*   [SQLite](https://www.sqlite.org/index.html)
*   [Pytest](https://pytest.org/)
*   [Playwright](https://playwright.dev/python/)
*   [Allure Report](https://allurereport.org/)
*   [Pydantic](https://pydantic-docs.helpmanual.io/)
*   [Jinja2](https://jinja.palletsprojects.com/)