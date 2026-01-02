import random
from typing import Optional, Dict
from database import get_connection
from models import AccountCreate, AccountUpdate


def generate_account_id() -> str:
    """Generate a unique 7-digit account ID"""
    conn = get_connection()
    cursor = conn.cursor()

    while True:
        account_id = str(random.randint(1000000, 9999999))
        cursor.execute("SELECT account_id FROM accounts WHERE account_id=?", (account_id,))
        if cursor.fetchone() is None:
            conn.close()
            return account_id


def create_account(account: AccountCreate) -> Dict:
    """Create a new account"""
    conn = get_connection()
    cursor = conn.cursor()

    account_id = generate_account_id()

    cursor.execute(
        """INSERT INTO accounts 
        (account_id, account_holder_name, email, phone, address, account_type, balance, date_opened, status) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (account_id, account.account_holder_name, account.email, account.phone,
         account.address, account.account_type, account.balance, account.date_opened, account.status)
    )

    conn.commit()
    conn.close()

    return {"account_id": account_id, "message": "Account created successfully"}


def get_account_by_id(account_id: str) -> Optional[Dict]:
    """Get account by account_id"""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM accounts WHERE account_id=?", (account_id,))
    row = cursor.fetchone()
    conn.close()

    if row is None:
        return None

    return {
        "account_id": row["account_id"],
        "account_holder_name": row["account_holder_name"],
        "email": row["email"],
        "phone": row["phone"],
        "address": row["address"],
        "account_type": row["account_type"],
        "balance": row["balance"],
        "date_opened": row["date_opened"],
        "status": row["status"]
    }


def update_account(account_id: str, account: AccountUpdate) -> bool:
    """Update an existing account"""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """UPDATE accounts SET 
        account_holder_name=?, email=?, phone=?, address=?, account_type=?, balance=?, date_opened=?, status=? 
        WHERE account_id=?""",
        (account.account_holder_name, account.email, account.phone, account.address,
         account.account_type, account.balance, account.date_opened, account.status, account_id)
    )

    conn.commit()
    rows_affected = cursor.rowcount
    conn.close()

    return rows_affected > 0


def delete_account(account_id: str) -> bool:
    """Delete an account"""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM accounts WHERE account_id=?", (account_id,))

    conn.commit()
    rows_affected = cursor.rowcount
    conn.close()

    return rows_affected > 0