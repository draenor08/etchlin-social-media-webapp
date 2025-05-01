from db.mysql_connection import get_connection

def get_flagged_posts():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM posts WHERE is_flagged = 1")
    posts = cursor.fetchall()
    cursor.close()
    conn.close()
    return posts

def resolve_flag(post_id, action):
    conn = get_connection()
    cursor = conn.cursor()
    if action == "delete":
        cursor.execute("DELETE FROM posts WHERE id = %s", (post_id,))
    elif action == "ignore":
        cursor.execute("UPDATE posts SET is_flagged = 0 WHERE id = %s", (post_id,))
    else:
        return False
    conn.commit()
    cursor.close()
    conn.close()
    return True
