import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "database.db")

def get_connection():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    # Updated schema with new columns
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

    conn.commit()
    conn.close()
    print("Database initialized successfully")

init_db()