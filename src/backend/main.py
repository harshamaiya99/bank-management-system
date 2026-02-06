# src/backend/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import uvicorn
import logging

from logging_config import setup_logging
from middleware import ObservabilityMiddleware
import database
from auth.router import router as auth_router
from accounts.router import router as accounts_router

setup_logging()
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Application starting up...")
    database.init_db()
    yield
    logger.info("Shutting down...")

app = FastAPI(
    title="Bank Management System",
    version="3.0.0",
    lifespan=lifespan
)

app.add_middleware(ObservabilityMiddleware)

# Enable CORS for the new Vite frontend (default port 5173)
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:9000",    # Backend (Swagger UI)
    "http://127.0.0.1:9000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(accounts_router)

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=9000, reload=True)