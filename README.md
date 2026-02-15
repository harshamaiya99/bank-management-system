# Bank Management System & Advanced QA Automation Framework
[![React](https://img.shields.io/badge/Frontend-React-61DAFB?style=flat-square&logo=react)](https://react.dev)
[![TypeScript](https://img.shields.io/badge/Language-TypeScript-3178C6?style=flat-square&logo=typescript)](https://www.typescriptlang.org/)
[![Vite](https://img.shields.io/badge/Tooling-Vite-646CFF?style=flat-square&logo=vite)](https://vitejs.dev/)
[![Tailwind CSS](https://img.shields.io/badge/CSS-Tailwind_CSS-06B6D4?style=flat-square&logo=tailwindcss)](https://tailwindcss.com/)
[![shadcn/ui](https://img.shields.io/badge/Components-shadcn%2Fui-000000?style=flat-square)](https://ui.shadcn.com/)
[![Radix UI](https://img.shields.io/badge/Accessibility-Radix_UI-161618?style=flat-square)](https://www.radix-ui.com/)
[![TanStack Query](https://img.shields.io/badge/State-TanStack_Query-FF4154?style=flat-square&logo=reactquery)](https://tanstack.com/query/latest)
[![Axios](https://img.shields.io/badge/HTTP-Axios-5A29E4?style=flat-square&logo=axios)](https://axios-http.com/)
[![React Hook Form](https://img.shields.io/badge/Form-React_Hook_Form-EC5990?style=flat-square&logo=reacthookform)](https://react-hook-form.com/)
[![Zod](https://img.shields.io/badge/Validation-Zod-3E67B1?style=flat-square)](https://zod.dev/)
[![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat-square&logo=python)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100.0-009688?style=flat-square&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Pydantic](https://img.shields.io/badge/Validation-Pydantic-2E8B57?style=flat-square&logo=pydantic)](https://docs.pydantic.dev/)
[![SQLite](https://img.shields.io/badge/Database-SQLite-003B57?style=flat-square&logo=sqlite)](https://www.sqlite.org/)
[![JWT](https://img.shields.io/badge/Auth-JWT-000000?style=flat-square&logo=jsonwebtokens)](https://jwt.io/)
[![bcrypt](https://img.shields.io/badge/Security-bcrypt-338033?style=flat-square)](https://pypi.org/project/bcrypt/)
[![Uvicorn](https://img.shields.io/badge/ASGI-Uvicorn-499848?style=flat-square)](https://www.uvicorn.org/)
[![Pytest](https://img.shields.io/badge/Tests-Pytest-009688?style=flat-square&logo=pytest)](https://docs.pytest.org/)
[![Karate](https://img.shields.io/badge/API_Testing-Karate-ED1C24?style=flat-square&logo=karate)](https://karatelabs.io/)
[![Playwright](https://img.shields.io/badge/UI_Testing-Playwright-2F80ED?style=flat-square&logo=playwright)](https://playwright.dev/)
[![Selenium](https://img.shields.io/badge/UI_Testing-Selenium-43B02A?style=flat-square&logo=selenium)](https://www.selenium.dev/)
[![Allure](https://img.shields.io/badge/Reporting-Allure_History-FF7700?style=flat-square&logo=allure)](https://allurereport.org/)
[![GitHub Actions](https://img.shields.io/badge/CI%2FCD-Composite_Actions-2088FF?style=flat-square&logo=github-actions)](https://docs.github.com/en/actions)



## Overview

This project is a full-stack **Bank Management System** designed to demonstrate a robust, production-ready **Test Automation Architecture**.

The application features a **FastAPI backend** with JWT authentication and a modern **React (Vite) frontend** styled with Tailwind CSS and Shadcn UI. However, the core value of this repository lies in its **quad-layer testing strategy**, implementing parallel testing frameworks to showcase modern best practices in QA engineering:

* **API Level:** Python (`Pytest` + `Requests`) vs. Java/JS (`Karate`)
* **UI Level:** Modern Async (`Playwright`) vs. Traditional Synchronous (`Selenium`)

---

## Key Features

### 1. Modern Full-Stack Architecture

* **Backend:** Built with **FastAPI**, featuring Pydantic validation, SQLite persistence, and structured logging.
* **Frontend:** A responsive Single Page Application (SPA) built with **React 19**, **TypeScript**, and **Vite**.
* **UI Components:** Utilizes **Shadcn UI** and **Tailwind CSS** for a professional, accessible design.
* **State Management:** Uses **TanStack Query** for efficient server-state synchronization.

### 2. Role-Based Access Control (RBAC)

* **Secure Auth:** JWT Authentication with `bcrypt` password hashing.
* **User Roles:**
* **Clerk:** Can View, Create, and Update accounts.
* **Manager:** Has all Clerk privileges plus **Delete** authority.



### 3. Advanced Design Patterns

* **Service Object Model (SOM):** API tests utilize a service layer to abstract HTTP requests (`tests/api_pytest/services/`).
* **Page Object Model (POM):** Both Playwright and Selenium suites utilize strict POM (`tests/web_*/pages/`) to separate page mechanics from test logic.

### 4. Intelligent Reporting & CI/CD

* **Allure History:** The CI pipeline automatically preserves test history, generating trend graphs (Pass/Fail ratios over time).
* **Screenshot on Failure:** Automatic capture of full-page screenshots attached to the Allure report whenever a UI test fails.
* **Composite Actions:** Modularized GitHub Actions for Setup, Restore History, and Reporting.

---

## Tech Stack

| Category | Technologies |
| --- | --- |
| **Backend** | Python, FastAPI, SQLite, Pydantic |
| **Frontend** | React, TypeScript, Vite, Tailwind CSS, Shadcn UI, React Hook Form, Zod |
| **API Testing** | Pytest, Requests, Karate (Java/JS) |
| **UI Testing** | Playwright (Python), Selenium WebDriver |
| **DevOps** | GitHub Actions, Allure Report |

---

## Project Structure

```text
.
├── .github
│   ├── actions                     # Reusable Composite Actions
│   │   ├── generate-report         # Allure Report generation logic
│   │   ├── restore-history         # Fetches history for trend analysis
│   │   ├── run-tests               # Test execution orchestration
│   │   └── setup-env               # Installs Python, Java, Node
│   └── workflows
│       └── main.yml                # Main CI/CD Pipeline
├── src
│   ├── backend                     # FastAPI Application
│   │   ├── accounts                # Domain: Accounts (CRUD, Routes, Schemas)
│   │   ├── auth                    # Domain: Auth (JWT, Login, Security)
│   │   ├── main.py                 # Application Entry Point
│   │   ├── database.py             # Database Connection & Session
│   │   └── middleware.py           # Observability & CORS
│   └── frontend                    # React (Vite) Application
│       ├── src
│       │   ├── api                 # Axios Client & Endpoints
│       │   ├── components          # Shared UI Components (Shadcn/UI)
│       │   ├── context             # Global State (AuthContext)
│       │   ├── hooks               # Custom React Hooks
│       │   ├── pages               # Route Views (Login, Dashboard, Create)
│       │   └── schemas             # Zod Validation Schemas
│       └── vite.config.ts          # Vite Configuration
├── tests                           # Quad-Layer Test Architecture
│   ├── api_karate                  # Layer 1: BDD API Tests (Java/Karate)
│   │   ├── src/test/java           # Feature files & Runners
│   │   └── test_karate_runner.py   # Pytest Wrapper for Karate
│   ├── api_pytest                  # Layer 2: Functional API Tests (Python)
│   │   ├── data                    # CSV Data Driven files
│   │   ├── services                # Service Object Model (HTTP Abstractions)
│   │   └── utils                   # Validators & Allure Helpers
│   ├── web_playwright              # Layer 3: Modern UI Tests (Playwright)
│   │   ├── data                    # CSV Test Data
│   │   ├── pages                   # Page Object Model (POM) Classes
│   │   └── test_e2e_flow.py        # Async End-to-End Tests
│   └── web_selenium                # Layer 4: Legacy UI Tests (Selenium)
│       ├── data                    # CSV Test Data
│       ├── pages                   # Page Object Model (POM) Classes
│       └── test_e2e_flow.py        # Sync End-to-End Tests
├── .env.example                    # Environment Variable Template
├── allurerc.yml                    # Allure Report Configuration
├── conftest.py                     # Global Pytest Fixtures & Hooks
├── pytest.ini                      # Pytest Configuration (Markers, Options)
└── requirements.txt                # Python Dependencies

```

---

## Getting Started

### Prerequisites

* **Python 3.10+**
* **Node.js 18+ & npm**
* **Java (JDK 11+)** (Required for Allure Reports & Karate)

### 1. Backend Setup

Navigate to the root directory and install Python dependencies:

```bash
# Create virtual environment (optional but recommended)
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

Start the Backend Server:

```bash

uvicorn main:app --app-dir src/backend --reload --port 9000
```

* **API Docs:** `http://localhost:9000/docs`
* **Health Check:** `http://localhost:9000/health`

### 2. Frontend Setup

Open a new terminal, navigate to the frontend directory, and install dependencies:

```bash

cd src/frontend
npm install
```

Start the Frontend Development Server:

```bash

npm run dev
```

* **Application URL:** `http://localhost:5173` (Proxies requests to port 9000)

---

## Running Tests

Ensure the backend server is running on port `9000` before executing tests.

### Option A: API Tests (Pytest)

Fast, comprehensive functional testing of API endpoints.

```bash 

pytest tests/api_pytest
```

### Option B: UI Tests (Playwright)

Modern, reliable end-to-end browser automation.

```bash
# Install browsers first
playwright install

# Run tests
pytest tests/web_playwright
```

### Option C: UI Tests (Selenium)

Modern, reliable end-to-end browser automation.

```bash
# Run tests
pytest tests/web_selenium
```

### Option D: API Tests (Karate)

BDD-style testing using Gherkin syntax.

```bash
# Runs via the Python wrapper
pytest tests/api_karate/test_karate_runner.py
```

### Option E: Run All Tests (CI Simulation)

To run all suites and generate a combined report:

```bash

pytest
```

---

## Default Credentials

The database is automatically seeded on startup with the following users:

| Role | Username | Password | Permissions |
| --- | --- | --- | --- |
| **Clerk** | `clerk` | `clerk123` | Read, Create, Update |
| **Manager** | `manager` | `manager123` | Read, Create, Update, **Delete** |

---

## CI/CD Pipeline

The project utilizes **GitHub Actions** for continuous integration. The workflow defined in `.github/workflows/main.yml`:

1. **Sets up** Python, Node, and Java environments.
2. **Restores** previous test history for trend analysis.
3. **Executes** all 4 test layers in parallel.
4. **Generates** an Allure report with history.
5. **Publishes** the report to a GitHub Pages branch (`allure-history`).