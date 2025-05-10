import json, os, uuid
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.db import connection
from utils.db import get_db_connection
from utils.auth import login_required_json
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

@csrf_exempt
@login_required_json
def like_post(request):
    if request.method == 'POST':
        user_id = request.session.get('user_id')
        data = json.loads(request.body)
        post_id = data['post_id']

        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM likes WHERE user_id = %s AND post_id = %s", (user_id, post_id))
            if cursor.fetchone():
                cursor.execute("DELETE FROM likes WHERE user_id = %s AND post_id = %s", (user_id, post_id))
                message = 'Unliked'
            else:
                cursor.execute("INSERT INTO likes (user_id, post_id) VALUES (%s, %s)", (user_id, post_id))
                message = 'Liked'
            conn.commit()
            return JsonResponse({'message': message})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
        finally:
            if 'cursor' in locals(): cursor.close()
            if 'conn' in locals(): conn.close()
    return JsonResponse({'error': 'Invalid method'}, status=405)
