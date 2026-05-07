import random
from database.db import get_connection

def check_coverage(address: str):
    zones = ["центр", "вулиця", "район"]

    if any(z in address.lower() for z in zones):
        return True
    return random.choice([True, True, False, False])

def check_internet_status(telegram_id: int):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT balance, status FROM users WHERE telegram_id = ?
    """, (telegram_id,))

    user = cur.fetchone()
    conn.close()

    if not user:
        return {
            "status": "unknown",
            "message": "Користувача не знайдено"
        }

    balance, status = user

    if balance <= 0:
        return {
            "status": "blocked",
            "message": "❌ У вас заборгованість. Поповніть баланс."
        }

    if random.randint(1, 10) == 1:
        return {
            "status": "outage",
            "message": "⚠️ У вашому районі аварія. Вже працюємо над відновленням."
        }
    return {
        "status": "ok",
        "message": "✔ Інтернет працює стабільно."
    }