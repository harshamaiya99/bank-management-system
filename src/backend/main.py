from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn
import os

# Import routes and database logic
from routes import api_router, html_router
import database

app = FastAPI(
    title="Bank Account Management System",
    description="Application for managing bank accounts",
    version="1.0.0"
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
# This allows us to access files in src/frontend via http://localhost:9000/static/filename.css
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # Points to src/
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")

app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")

# --- Startup Event (Auto-Initialize Database) ---
@app.on_event("startup")
def startup_event():
    print("Checking database connection...")
    # This will create tables and seed users (Clerk/Manager) if they don't exist
    database.init_db()
    print("Database initialized.")

# --- Register Routes ---
app.include_router(html_router)
app.include_router(api_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=9000, reload=True)