from db.mysql_connection import get_connection

def create_post(user_id, caption, image_url):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO post (user_id, caption, image_url)
            VALUES (%s, %s, %s)
        """, (user_id, caption, image_url))
        conn.commit()
    finally:
        cursor.close()
        conn.close()

def get_user_posts(user_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM post WHERE user_id = %s", (user_id,))
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()

def delete_post(post_id):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM post WHERE post_id = %s", (post_id,))
        conn.commit()
    finally:
        cursor.close()
        conn.close()

def get_comments_for_post(post_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM comment WHERE post_id = %s", (post_id,))
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()
