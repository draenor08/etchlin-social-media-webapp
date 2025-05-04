from django.views.decorators.csrf import csrf_exempt
from utils.auth import login_required_json
from utils.db import get_db_connection
from django.http import JsonResponse
import os, uuid, json
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

@csrf_exempt
@login_required_json
def create_comment(request):
    if request.method == 'POST':
        user_id = request.session.get('user_id')
        data = json.loads(request.body)
        post_id = data['post_id']
        comment_text = data['comment']

        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO comment (user_id, post_id, text) VALUES (%s, %s, %s)",
                           (user_id, post_id, comment_text))
            conn.commit()
            return JsonResponse({'message': 'Comment added'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
        finally:
            if 'cursor' in locals(): cursor.close()
            if 'conn' in locals(): conn.close()
    return JsonResponse({'error': 'Invalid method'}, status=405)