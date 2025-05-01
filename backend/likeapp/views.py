import uuid
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.db import connection

@csrf_exempt
def create_like(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        post_id = request.POST.get('post_id')

        if not user_id or not post_id:
            return JsonResponse({'error': 'user_id and post_id required'}, status=400)

        like_id = str(uuid.uuid4())[:24]
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO likes (like_id, post_id, user_id)
                VALUES (%s, %s, %s)
            """, [like_id, post_id, user_id])

        return JsonResponse({'success': True, 'like_id': like_id})
    
    return JsonResponse({'error': 'Only POST allowed'}, status=405)
