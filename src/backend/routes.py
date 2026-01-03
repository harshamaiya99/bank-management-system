from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import List
import os
from models import AccountCreate, AccountUpdate, AccountResponse
import crud

# Setup templates
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "frontend"))

# Create routers
html_router = APIRouter()
api_router = APIRouter(prefix="/accounts", tags=["accounts"])

# HTML Routes
@html_router.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@html_router.get("/accountDetails.html", response_class=HTMLResponse)
def account_details_page(request: Request):
    return templates.TemplateResponse("accountDetails.html", {"request": request})

@html_router.get("/createAccount.html", response_class=HTMLResponse)
def create_account_page(request: Request):
    return templates.TemplateResponse("createAccount.html", {"request": request})

# API Routes
@api_router.get("", response_model=List[AccountResponse])
def get_all_accounts():
    """Get all accounts"""
    accounts = crud.get_all_accounts()
    return accounts

@api_router.post("", status_code=200)
def create_account(account: AccountCreate):
    """Create a new account"""
    result = crud.create_account(account)
    return result

@api_router.get("/{account_id}", response_model=AccountResponse)
def get_account(account_id: str):
    """Get account by ID"""
    account = crud.get_account_by_id(account_id)
    if account is None:
        raise HTTPException(status_code=404, detail="Account not found")
    return account

@api_router.put("/{account_id}")
def update_account(account_id: str, account: AccountUpdate):
    """Update an existing account"""
    success = crud.update_account(account_id, account)
    if not success:
        raise HTTPException(status_code=404, detail="Account not found")
    return {"message": "Account updated successfully"}

@api_router.delete("/{account_id}")
def delete_account(account_id: str):
    """Delete an account"""
    success = crud.delete_account(account_id)
    if not success:
        raise HTTPException(status_code=404, detail="Account not found")
    return {"message": "Account deleted successfully"}