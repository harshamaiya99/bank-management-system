from pydantic import BaseModel
from typing import Optional

class AccountCreate(BaseModel):
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

class AccountResponse(BaseModel):
    account_id: str
    account_holder_name: str
    email: str
    phone: str
    address: str
    account_type: str
    balance: float
    date_opened: str
    status: str