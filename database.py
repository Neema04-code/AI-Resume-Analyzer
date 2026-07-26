import sqlite3

conn = sqlite3.connect("users.db")

cursor = conn.cursor()


# Users table
cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)
""")


# History table
cursor.execute("""
CREATE TABLE IF NOT EXISTS history(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_name TEXT NOT NULL,
    score INTEGER,
    skills TEXT,
    missing TEXT,
    jobs TEXT,
    date_time TEXT
""")


conn.commit()
conn.close()

print("Database updated successfully")