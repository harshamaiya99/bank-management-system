from fastapi import APIRouter, HTTPException, Request, Depends, status
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates
from typing import List
import os
from datetime import timedelta

# Import Models & Logic
from models import AccountCreate, AccountUpdate, AccountResponse, Token, User
import crud
import auth

# Setup Templates
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "frontend"))

# Create Routers
html_router = APIRouter()
api_router = APIRouter(prefix="/accounts", tags=["accounts"])


# ==========================
#      HTML ROUTES
# ==========================

@html_router.get("/login.html", response_class=HTMLResponse)
def login_page(request: Request):
    """Serves the Login Page"""
    return templates.TemplateResponse("login.html", {"request": request})


@html_router.get("/", response_class=HTMLResponse)
def home(request: Request):
    """
    Serves the Home/Dashboard Page.
    Points to home_page.html (formerly index.html).
    """
    return templates.TemplateResponse("home_page.html", {"request": request})


@html_router.get("/accountDetails.html", response_class=HTMLResponse)
def account_details_page(request: Request):
    """Serves the Details/Update Page"""
    return templates.TemplateResponse("accountDetails.html", {"request": request})


@html_router.get("/createAccount.html", response_class=HTMLResponse)
def create_account_page(request: Request):
    """Serves the Creation Page"""
    return templates.TemplateResponse("createAccount.html", {"request": request})


# ==========================
#      AUTH ROUTES
# ==========================

@html_router.post("/token", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Validates username/password and issues a JWT token.
    """
    user = crud.get_user_by_username(form_data.username)
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.username, "role": user.role},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer", "role": user.role}


# ==========================
#      API ROUTES (SECURE)
# ==========================

@api_router.get("", response_model=List[AccountResponse])
def get_all_accounts(current_user: User = Depends(auth.get_current_user)):
    """Auth: Clerk, Manager"""
    accounts = crud.get_all_accounts()
    return accounts


@api_router.post("", status_code=200)
def create_account(account: AccountCreate, current_user: User = Depends(auth.get_current_user)):
    """Auth: Clerk, Manager"""
    result = crud.create_account(account)
    return result


@api_router.get("/{account_id}", response_model=AccountResponse)
def get_account(account_id: str, current_user: User = Depends(auth.get_current_user)):
    """Auth: Clerk, Manager"""
    account = crud.get_account_by_id(account_id)
    if account is None:
        raise HTTPException(status_code=404, detail="Account not found")
    return account


@api_router.put("/{account_id}")
def update_account(account_id: str, account: AccountUpdate, current_user: User = Depends(auth.get_current_user)):
    """Auth: Clerk, Manager"""
    success = crud.update_account(account_id, account)
    if not success:
        raise HTTPException(status_code=404, detail="Account not found")
    return {"message": "Account updated successfully"}


@api_router.delete("/{account_id}")
def delete_account(account_id: str, current_user: User = Depends(auth.get_current_user)):
    """Auth: MANAGER ONLY"""
    if current_user.role != "manager":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Operation not permitted"
        )

    success = crud.delete_account(account_id)
    if not success:
        raise HTTPException(status_code=404, detail="Account not found")
    return {"message": "Account deleted successfully"}