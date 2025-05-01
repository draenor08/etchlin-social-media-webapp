from db.mysql_connection import get_connection

def send_friend_request(requester_id, receiver_id):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO friends (request, acceptance, status)
            VALUES (%s, %s, 'pending')
        """, (requester_id, receiver_id))
        conn.commit()
    finally:
        cursor.close()
        conn.close()

def accept_friend_request(requester_id, receiver_id):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            UPDATE friends
            SET status = 'accepted'
            WHERE request = %s AND acceptance = %s
        """, (requester_id, receiver_id))
        conn.commit()
    finally:
        cursor.close()
        conn.close()

def get_friends_list(user_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT u.* FROM friends f
            JOIN user u ON (f.request = u.user_id OR f.acceptance = u.user_id)
            WHERE (f.request = %s OR f.acceptance = %s)
              AND f.status = 'accepted'
        """, (user_id, user_id))
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()
