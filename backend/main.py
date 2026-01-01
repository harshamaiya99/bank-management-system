from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import sqlite3
import os
import random

app = FastAPI()
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "frontend"))

# Database
conn = sqlite3.connect(os.path.join(BASE_DIR, "database.db"), check_same_thread=False)
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS accounts (
    account_id TEXT PRIMARY KEY,
    account_holder_name TEXT NOT NULL,
    email TEXT NOT NULL,
    phone TEXT NOT NULL,
    address TEXT NOT NULL,
    account_type TEXT NOT NULL,
    balance REAL NOT NULL DEFAULT 0.0,
    date_opened TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'Active'
)
""")
conn.commit()

class Account(BaseModel):
    account_holder_name: str
    email: str
    phone: str
    address: str
    account_type: str
    balance: float = 0.0
    date_opened: str
    status: str = "Active"

class AccountUpdate(BaseModel):
    account_holder_name: str
    email: str
    phone: str
    address: str
    account_type: str
    balance: float
    date_opened: str
    status: str

def generate_account_id():
    while True:
        account_id = str(random.randint(1000000, 9999999))
        cursor.execute("SELECT account_id FROM accounts WHERE account_id=?", (account_id,))
        if cursor.fetchone() is None:
            return account_id

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/accountDetails.html", response_class=HTMLResponse)
def account_details_page(request: Request):
    return templates.TemplateResponse("accountDetails.html", {"request": request})

@app.get("/createAccount.html", response_class=HTMLResponse)
def create_account_page(request: Request):
    return templates.TemplateResponse("createAccount.html", {"request": request})

# CREATE
@app.post("/accounts")
def create_account(account: Account):
    account_id = generate_account_id()
    cursor.execute(
        """INSERT INTO accounts 
        (account_id, account_holder_name, email, phone, address, account_type, balance, date_opened, status) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (account_id, account.account_holder_name, account.email, account.phone,
         account.address, account.account_type, account.balance, account.date_opened, account.status)
    )
    conn.commit()
    return {"message": "Account created successfully", "account_id": account_id}

# READ by account_id
@app.get("/accounts/{account_id}")
def get_account(account_id: str):
    cursor.execute("SELECT * FROM accounts WHERE account_id=?", (account_id,))
    row = cursor.fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="Account not found")
    return {
        "account_id": row[0],
        "account_holder_name": row[1],
        "email": row[2],
        "phone": row[3],
        "address": row[4],
        "account_type": row[5],
        "balance": row[6],
        "date_opened": row[7],
        "status": row[8]
    }


@app.get("/accounts")
def get_all_accounts():
    cursor.execute("SELECT * FROM accounts")
    rows = cursor.fetchall()

    accounts = []
    for row in rows:
        accounts.append({
            "account_id": row[0],
            "account_holder_name": row[1],
            "email": row[2],
            "phone": row[3],
            "address": row[4],
            "account_type": row[5],
            "balance": row[6],
            "date_opened": row[7],
            "status": row[8]
        })

    return accounts

# UPDATE
@app.put("/accounts/{account_id}")
def update_account(account_id: str, account: AccountUpdate):
    cursor.execute(
        """UPDATE accounts SET 
        account_holder_name=?, email=?, phone=?, address=?, account_type=?, balance=?, date_opened=?, status=? 
        WHERE account_id=?""",
        (account.account_holder_name, account.email, account.phone, account.address,
         account.account_type, account.balance, account.date_opened, account.status, account_id)
    )
    conn.commit()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Account not found")
    return {"message": "Account updated successfully"}

# DELETE
@app.delete("/accounts/{account_id}")
def delete_account(account_id: str):
    cursor.execute("DELETE FROM accounts WHERE account_id=?", (account_id,))
    conn.commit()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Account not found")
    return {"message": "Account deleted successfully"}