from database.db import get_connection

def get_or_create_user(telegram_id: int):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM users WHERE telegram_id = ?", (telegram_id,))
    user = cur.fetchone()

    if not user:
        cur.execute("""
            INSERT INTO users (telegram_id, balance, tariff, status, next_payment)
            VALUES (?, 0, 'Basic', 'online', '2026-06-01')
        """, (telegram_id,))
        conn.commit()

        cur.execute("SELECT * FROM users WHERE telegram_id = ?", (telegram_id,))
        user = cur.fetchone()

    conn.close()
    return user

import sqlite3
from database.db import get_connection


def get_user(telegram_id: int):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT telegram_id, balance, tariff FROM users WHERE telegram_id = ?", (telegram_id,))
    user = cur.fetchone()

    conn.close()
    return user


def create_user_if_not_exists(telegram_id: int):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("INSERT OR IGNORE INTO users (telegram_id) VALUES (?)", (telegram_id,))

    conn.commit()
    conn.close()


def update_tariff(telegram_id: int, tariff: str):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("UPDATE users SET tariff = ? WHERE telegram_id = ?", (tariff, telegram_id))

    conn.commit()
    conn.close()


def get_balance(telegram_id: int):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT balance FROM users WHERE telegram_id = ?", (telegram_id,))
    result = cur.fetchone()

    conn.close()
    return result[0] if result else 0


def update_balance(telegram_id: int, new_balance: float):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("UPDATE users SET balance = ? WHERE telegram_id = ?", (new_balance, telegram_id))

    conn.commit()
    conn.close()