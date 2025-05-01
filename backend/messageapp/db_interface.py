from db.mysql_connection import get_connection

def send_message(sender_id, receiver_id, text):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO message (sender_id, receiver_id, text)
            VALUES (%s, %s, %s)
        """, (sender_id, receiver_id, text))
        conn.commit()
    finally:
        cursor.close()
        conn.close()

def get_messages_between_users(user1_id, user2_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT * FROM message
            WHERE (sender_id = %s AND receiver_id = %s)
            OR (sender_id = %s AND receiver_id = %s)
        """, (user1_id, user2_id, user2_id, user1_id))
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()
