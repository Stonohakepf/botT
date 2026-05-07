import uuid
import time
from database.db import get_connection

def confirm_payment(telegram_id: int, amount: float):

    conn = get_connection()
    cur = conn.cursor()

    try:
        # 1. оновити баланс
        cur.execute("""
            UPDATE users
            SET balance = balance + ?
            WHERE telegram_id = ?
        """, (amount, telegram_id))

        # 2. оновити останній платіж
        cur.execute("""
            UPDATE payments
            SET status = 'success'
            WHERE id = (
                SELECT id FROM payments
                WHERE user_id = (
                    SELECT id FROM users WHERE telegram_id = ?
                )
                ORDER BY id DESC
                LIMIT 1
            )
        """, (telegram_id,))

        conn.commit()

    finally:
        conn.close()

    return True