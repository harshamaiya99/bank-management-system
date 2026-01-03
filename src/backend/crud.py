import random
from typing import Optional, Dict, List
from database import get_connection
from models import AccountCreate, AccountUpdate

def generate_account_id() -> str:
    conn = get_connection()
    cursor = conn.cursor()
    while True:
        account_id = str(random.randint(1000000, 9999999))
        cursor.execute("SELECT account_id FROM accounts WHERE account_id=?", (account_id,))
        if cursor.fetchone() is None:
            conn.close()
            return account_id

def create_account(account: AccountCreate) -> Dict:
    conn = get_connection()
    cursor = conn.cursor()
    account_id = generate_account_id()

    cursor.execute(
        """INSERT INTO accounts 
        (account_id, account_holder_name, dob, gender, email, phone, address, zip_code, 
         account_type, balance, date_opened, status, services, marketing_opt_in, agreed_to_terms) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (account_id, account.account_holder_name, account.dob, account.gender,
         account.email, account.phone, account.address, account.zip_code,
         account.account_type, account.balance, account.date_opened, account.status,
         account.services, account.marketing_opt_in, account.agreed_to_terms)
    )
    conn.commit()
    conn.close()
    return {"account_id": account_id, "message": "Account created successfully"}

def get_all_accounts() -> List[Dict]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM accounts")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_account_by_id(account_id: str) -> Optional[Dict]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM accounts WHERE account_id=?", (account_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

def update_account(account_id: str, account: AccountUpdate) -> bool:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """UPDATE accounts SET 
        account_holder_name=?, dob=?, gender=?, email=?, phone=?, address=?, zip_code=?, 
        account_type=?, balance=?, date_opened=?, status=?, services=?, marketing_opt_in=?
        WHERE account_id=?""",
        (account.account_holder_name, account.dob, account.gender, account.email, account.phone,
         account.address, account.zip_code, account.account_type, account.balance,
         account.date_opened, account.status, account.services, account.marketing_opt_in, account_id)
    )
    conn.commit()
    rows_affected = cursor.rowcount
    conn.close()
    return rows_affected > 0

def delete_account(account_id: str) -> bool:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM accounts WHERE account_id=?", (account_id,))
    conn.commit()
    rows_affected = cursor.rowcount
    conn.close()
    return rows_affected > 0