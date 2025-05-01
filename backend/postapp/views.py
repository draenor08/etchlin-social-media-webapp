import os
import uuid
from django.db import connection
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

@csrf_exempt
def user_feed(request):
    if request.method == 'GET':
        user_id = request.GET.get('user_id')
        if not user_id:
            return JsonResponse({'error': 'user_id is required'}, status=400)

        feed = []
        with connection.cursor() as cursor:
            # Fetch posts from friends (both directions)
            cursor.execute("""
                SELECT p.post_id, p.user_id, p.caption, p.image_url, p.timestamp,
                       u.first_name, u.profile_picture
                FROM post p
                JOIN user u ON p.user_id = u.user_id
                JOIN friends f ON (
                    (f.request = %s AND f.acceptance = p.user_id) OR 
                    (f.acceptance = %s AND f.request = p.user_id)
                )
                WHERE f.status = 'accepted'
                ORDER BY p.timestamp DESC
            """, [user_id, user_id])
            posts = cursor.fetchall()

            for post in posts:
                post_id, author_id, caption, image_url, timestamp, first_name, profile_picture = post

                # Get comment count
                cursor.execute("SELECT COUNT(*) FROM comment WHERE post_id = %s", [post_id])
                comment_count = cursor.fetchone()[0]

                # Get like count
                cursor.execute("SELECT COUNT(*) FROM likes WHERE post_id = %s", [post_id])
                like_count = cursor.fetchone()[0]

                # Get comments
                cursor.execute("""
                    SELECT c.comment_id, c.user_id, u.first_name, u.profile_picture, c.content, c.timestamp
                    FROM comment c
                    JOIN user u ON c.user_id = u.user_id
                    WHERE c.post_id = %s
                    ORDER BY c.timestamp ASC
                """, [post_id])
                comments_raw = cursor.fetchall()

                comments = [
                    {
                        'comment_id': c[0],
                        'user_id': c[1],
                        'first_name': c[2],
                        'profile_picture': c[3],
                        'content': c[4],
                        'timestamp': c[5].isoformat()
                    }
                    for c in comments_raw
                ]

                feed.append({
                    'post_id': post_id,
                    'user_id': author_id,
                    'first_name': first_name,
                    'profile_picture': profile_picture,
                    'caption': caption,
                    'image_url': image_url,
                    'timestamp': timestamp.isoformat(),
                    'like_count': like_count,
                    'comment_count': comment_count,
                    'comments': comments
                })

        return JsonResponse({'feed': feed})
    
    return JsonResponse({'error': 'Only GET method allowed'}, status=405)

