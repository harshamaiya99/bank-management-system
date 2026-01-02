from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import html_router, api_router

app = FastAPI(
    title="Bank Account Management API",
    description="API for managing bank accounts",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(html_router)
app.include_router(api_router)

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=9000)