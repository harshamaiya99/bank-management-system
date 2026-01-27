from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from contextlib import asynccontextmanager
import uvicorn
import os
import logging

# --- 1. NEW IMPORTS FOR OBSERVABILITY ---
from logging_config import setup_logging
from middleware import ObservabilityMiddleware

# --- EXISTING IMPORTS ---
import database
from auth.router import router as auth_router
from accounts.router import router as accounts_router
from routes_html import router as html_router

# --- 2. SETUP LOGGING (Before App Starts) ---
setup_logging()
logger = logging.getLogger(__name__)


# --- 3. LIFESPAN (Modern replacement for @app.on_event) ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup Logic
    logger.info("Application starting up...")
    print("Checking database connection...")
    database.init_db()
    print("Database initialized.")

    yield  # Application runs here

    # Shutdown Logic (Optional)
    logger.info("Shutting down...")


# --- APP DEFINITION ---
app = FastAPI(
    title="Bank Management System",
    description="Application for Managing Bank accounts & Advanced QA Automation Framework",
    version="2.0.0",
    lifespan=lifespan  # Link the lifespan logic here
)

# --- MIDDLEWARE CONFIGURATION ---

# 1. Observability Middleware (MUST BE FIRST to catch everything)
app.add_middleware(ObservabilityMiddleware)

# 2. CORS Configuration (Your specific settings)
origins = [
    "http://localhost:9000",
    "http://127.0.0.1:9000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- STATIC FILES (Your existing setup) ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Points to src/
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")

app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")

# --- REGISTER ROUTES ---
app.include_router(auth_router)
app.include_router(accounts_router)
app.include_router(html_router)

# --- Health check endpoint ---
@app.get("/health")
def health_check():
    return {"status": "healthy"}

# include_in_schema=False hides this from the Swagger UI (/docs)
@app.get("/", include_in_schema=False)
def root():
    """Redirects root path to login page"""
    return RedirectResponse(url="/login.html")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=9000, reload=True)