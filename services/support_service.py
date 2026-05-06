from database.db import get_connection


def create_ticket(telegram_id: int, problem_type: str, description: str = ""):
    conn = get_connection()
    cur = conn.cursor()
    
    cur.execute("SELECT id FROM users WHERE telegram_id = ?", (telegram_id,))
    user = cur.fetchone()

    if not user:
        conn.close()
        return False

    user_id = user[0]

    cur.execute("""
        INSERT INTO tickets (user_id, problem_type, description, status)
        VALUES (?, ?, ?, 'open')
    """, (user_id, problem_type, description))

    conn.commit()
    conn.close()

    return True