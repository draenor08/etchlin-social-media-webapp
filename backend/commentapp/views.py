from django.views.decorators.csrf import csrf_exempt
from utils.auth import login_required_json
from utils.db import get_db_connection
from django.http import JsonResponse
import json

@csrf_exempt
@login_required_json
def create_comment(request):
    if request.method == 'POST':
        try:
            user_id = request.session.get('user_id')
            data = json.loads(request.body)

            # Extracting post_id and content from the request
            post_id = data.get('post_id')
            comment_content = data.get('content')

            if not post_id or not comment_content:
                return JsonResponse({'error': 'Missing post_id or content'}, status=400)

            conn = get_db_connection()
            cursor = conn.cursor()

            # Insert the comment into the database
            cursor.execute("""
                INSERT INTO comment (post_id, user_id, content, is_blurred, timestamp)
                VALUES (%s, %s, %s, %s, NOW())
            """, (post_id, user_id, comment_content, 0))
            conn.commit()
            comment_id = cursor.lastrowid

            # Fetch the new comment details for the response
            cursor.execute("""
                SELECT c.comment_id, c.content, c.timestamp, u.first_name, u.profile_picture
                FROM comment c
                JOIN user u ON c.user_id = u.user_id
                WHERE c.comment_id = %s
            """, (comment_id,))
            new_comment = cursor.fetchone()

            comment_data = {
                'comment_id': new_comment[0],
                'content': new_comment[1],
                'timestamp': new_comment[2].isoformat(),
                'first_name': new_comment[3],
                'profile_picture': f"/assets/person/{new_comment[4]}" if new_comment[4] else "/assets/default_profile.png"
            }

            return JsonResponse(comment_data)

        except Exception as e:
            print("Error creating comment:", str(e))
            return JsonResponse({'error': str(e)}, status=500)
        finally:
            if 'cursor' in locals(): cursor.close()
            if 'conn' in locals(): conn.close()
    
    return JsonResponse({'error': 'Invalid method'}, status=405)
