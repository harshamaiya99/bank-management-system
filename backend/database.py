import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "database.db")


def get_connection():
    """Get database connection"""
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initialize database with tables"""
    conn = get_connection()
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
    conn.close()
    print("Database initialized successfully")


# Initialize database when module is imported
init_db()