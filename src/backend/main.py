from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn
import os
import database

# Import Routers from new folder structure
from auth.router import router as auth_router
from accounts.router import router as accounts_router
from routes_html import router as html_router

app = FastAPI(
    title="Bank Management System",
    description="Application for Managing Bank accounts & Advanced QA Automation Framework",
    version="2.0.0"
)

# --- CORS Configuration ---
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

# --- Mount Static Files (CSS/JS) ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # Points to src/
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")

app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")

# --- Startup Event ---
@app.on_event("startup")
def startup_event():
    print("Checking database connection...")
    database.init_db()
    print("Database initialized.")

# --- Register Routes ---
app.include_router(auth_router)
app.include_router(accounts_router)
app.include_router(html_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=9000, reload=True)