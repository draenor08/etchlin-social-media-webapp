import os
from django.db import connection
from django.views.decorators.csrf import csrf_exempt
from utils.auth import login_required_json
from utils.db import get_db_connection
from django.http import JsonResponse
import os, uuid, json
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

# CREATE POST (TEXT/IMAGE)
@csrf_exempt
@login_required_json
def create_post(request):
    if request.method == 'POST':
        user_id = request.session.get('user_id')
        caption = request.POST.get('caption', '')
        image_file = request.FILES.get('image', None)

        image_path = None
        if image_file:
            file_ext = os.path.splitext(image_file.name)[-1]
            file_name = f"post_{uuid.uuid4().hex}{file_ext}"
            image_path = os.path.join('posts', file_name)
            default_storage.save(image_path, ContentFile(image_file.read()))

        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO post (user_id, caption, image_path) VALUES (%s, %s, %s)",
                (user_id, caption, image_path)
            )
            conn.commit()
            return JsonResponse({'message': 'Post created'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
        finally:
            if 'cursor' in locals(): cursor.close()
            if 'conn' in locals(): conn.close()
    return JsonResponse({'error': 'Invalid request'}, status=400)

@csrf_exempt
@login_required_json
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

