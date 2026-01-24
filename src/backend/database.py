import sqlite3
import os
from passlib.context import CryptContext

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "database.db")

# Setup hashing for seeding
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_connection():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    # Existing accounts table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS accounts (
        account_id TEXT PRIMARY KEY,
        account_holder_name TEXT NOT NULL,
        dob TEXT NOT NULL,
        gender TEXT NOT NULL,
        email TEXT NOT NULL,
        phone TEXT NOT NULL,
        address TEXT NOT NULL,
        zip_code TEXT NOT NULL,
        account_type TEXT NOT NULL,
        balance REAL NOT NULL DEFAULT 0.0,
        date_opened TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'Active',
        services TEXT,
        marketing_opt_in BOOLEAN NOT NULL DEFAULT 0,
        agreed_to_terms BOOLEAN NOT NULL DEFAULT 0
    )
    """)

    # NEW: Users table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        hashed_password TEXT NOT NULL,
        role TEXT NOT NULL
    )
    """)

    # Seed Default Users (if not exist)
    # Clerk: clerk / clerk123
    # Manager: manager / manager123
    clerk_pw = pwd_context.hash("clerk123")
    manager_pw = pwd_context.hash("manager123")

    cursor.execute("INSERT OR IGNORE INTO users (username, hashed_password, role) VALUES (?, ?, ?)",
                   ("clerk", clerk_pw, "clerk"))
    cursor.execute("INSERT OR IGNORE INTO users (username, hashed_password, role) VALUES (?, ?, ?)",
                   ("manager", manager_pw, "manager"))

    conn.commit()
    conn.close()
    print("Database initialized successfully with Users table.")


if __name__ == "__main__":
    init_db()