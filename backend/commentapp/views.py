import uuid
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.db import connection

@csrf_exempt
def create_comment(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        post_id = request.POST.get('post_id')
        content = request.POST.get('content', '')

        if not user_id or not post_id or not content:
            return JsonResponse({'error': 'user_id, post_id, and content required'}, status=400)

        comment_id = str(uuid.uuid4())[:20]
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO comment (comment_id, post_id, user_id, content)
                VALUES (%s, %s, %s, %s)
            """, [comment_id, post_id, user_id, content])

        return JsonResponse({'success': True, 'comment_id': comment_id})
    
    return JsonResponse({'error': 'Only POST allowed'}, status=405)
