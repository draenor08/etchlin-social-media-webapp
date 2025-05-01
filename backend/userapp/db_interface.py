from db.mysql_connection import get_connection

def get_user_by_email(email):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM user WHERE email = %s", (email,))
        return cursor.fetchone()
    finally:
        cursor.close()
        conn.close()

def create_user(first_name, last_name, email, password, date_of_birth):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO user (first_name, last_name, email, password, date_of_birth)
            VALUES (%s, %s, %s, %s, %s)
        """, (first_name, last_name, email, password, date_of_birth))
        conn.commit()
    finally:
        cursor.close()
        conn.close()

def update_user_bio(user_id, bio):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            UPDATE user
            SET bio = %s
            WHERE user_id = %s
        """, (bio, user_id))
        conn.commit()
    finally:
        cursor.close()
        conn.close()
