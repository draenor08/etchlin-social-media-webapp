import os
import uuid
import pymysql
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage
from django.utils import timezone

@csrf_exempt
def create_post(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        caption = request.POST.get('caption', '')
        image = request.FILES.get('image')

        if not user_id or not image:
            return JsonResponse({'error': 'user_id and image are required'}, status=400)

        post_id = str(uuid.uuid4().hex[:16])
        image_name = f"{post_id}_{image.name}"
        image_path = os.path.join(settings.MEDIA_ROOT, 'posts', image_name)

        os.makedirs(os.path.dirname(image_path), exist_ok=True)
        fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'posts'))
        fs.save(image_name, image)

        image_url = f"/media/posts/{image_name}"
        timestamp = timezone.now()

        try:
            conn = pymysql.connect(
                host='localhost',
                user=os.getenv("MYSQL_USER"),
                password=os.getenv("MYSQL_PASSWORD"),
                database=os.getenv("MYSQL_DB")
            )
            cursor = conn.cursor()
            sql = """
                INSERT INTO post (post_id, user_id, caption, image_url, timestamp)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (post_id, user_id, caption, image_url, timestamp))
            conn.commit()
            cursor.close()
            conn.close()
            return JsonResponse({'message': 'Post created successfully', 'post_id': post_id}, status=201)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=405)