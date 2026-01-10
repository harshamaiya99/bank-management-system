from pydantic import BaseModel
from typing import Optional

class AccountCreate(BaseModel):
    # Personal Identity
    account_holder_name: str
    dob: str
    gender: str

    # Contact Information
    email: str
    phone: str
    address: str
    zip_code: str

    # Account Details
    account_type: str
    balance: float = 0.0
    status: str = "Active"

    # Preferences / Checkboxes
    services: str  # Stores comma-separated values (e.g., "SMS,DebitCard")
    marketing_opt_in: bool
    agreed_to_terms: bool

class AccountUpdate(BaseModel):
    account_holder_name: str
    dob: str
    gender: str
    email: str
    phone: str
    address: str
    zip_code: str
    account_type: str
    balance: float
    status: str
    services: str
    marketing_opt_in: bool

class AccountResponse(BaseModel):
    account_id: str
    account_holder_name: str
    dob: str
    gender: str
    email: str
    phone: str
    address: str
    zip_code: str
    account_type: str
    balance: float
    date_opened: str
    status: str
    services: str
    marketing_opt_in: bool
    agreed_to_terms: bool