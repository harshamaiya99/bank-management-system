uvicorn main:app --app-dir src/backend --reload --port 9000

C:\Users\maiya>netstat -ano | findstr :9000
  TCP    127.0.0.1:9000         0.0.0.0:0              LISTENING       23996

C:\Users\maiya>taskkill /PID 23996 /F
SUCCESS: The process with PID 23996 has been terminated.

You have 3 easy ways to check database.db.

✅ OPTION 1 (BEST & SIMPLE): Check via Python (Recommended)

From your project root:

python


Then run:

import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

cursor.execute("SELECT * FROM accounts")
rows = cursor.fetchall()

for row in rows:
    print(row)

conn.close()

✅ Expected output
(1, 'Harsha', 'harsha@email.com')
(2, 'Test User', 'test@email.com')


This confirms:

Data exists

Table is correct

Backend wrote to DB

✅ OPTION 2: Use DB Browser for SQLite (Visual – very clear)

Best if you like GUI.

Steps:

Download DB Browser for SQLite (free)

Open it

Click Open Database

Select:

web-FastAPI-SQLlite/database.db


Go to Browse Data

Select table: accounts

You’ll see all rows visually 👀

✅ OPTION 3: Verify via API (Most realistic)

Let’s add a quick endpoint to view accounts.

Add this to backend/main.py:
@app.get("/accounts")
def get_accounts():
    cursor.execute("SELECT * FROM accounts")
    rows = cursor.fetchall()
    return [
        {"id": r[0], "name": r[1], "email": r[2]}
        for r in rows
    ]


Restart server, then open:

http://127.0.0.1:9000/accounts


You’ll see JSON like:

[
  {
    "id": 1,
    "name": "Harsha",
    "email": "harsha@email.com"
  }
]


This is how real backend APIs are validated.