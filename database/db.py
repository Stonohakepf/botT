import sqlite3

DB_PATH = "database/db.sqlite"

def get_connection():
    conn = sqlite3.connect(
        DB_PATH,
        timeout=10,
        check_same_thread=False
    )
    conn.execute("PRAGMA journal_mode=WAL;")
    return conn

def init_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        telegram_id INTEGER UNIQUE,
        balance REAL DEFAULT 0,
        tariff TEXT DEFAULT 'Basic',
        status TEXT DEFAULT 'offline',
        next_payment TEXT DEFAULT 'not set'
    )
    """)

    conn.commit()
    conn.close()