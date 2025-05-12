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
            # Force images to be saved in the 'post/' subdirectory
            file_ext = os.path.splitext(image_file.name)[-1]
            file_name = f"post_{uuid.uuid4().hex}{file_ext}"
            image_path = os.path.join('post', file_name)
            default_storage.save(os.path.join('post', file_name), ContentFile(image_file.read()))

        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO post (user_id, caption, image_url) VALUES (%s, %s, %s)",
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
def update_post(request):
    try:
        if request.method != 'PATCH':
            return JsonResponse({'error': 'Only PATCH method allowed'}, status=405)

        user_id = request.session.get('user_id')
        data = json.loads(request.body)
        post_id = data.get('post_id')
        new_caption = data.get('caption')

        if not post_id or not new_caption:
            return JsonResponse({'error': 'post_id and caption are required'}, status=400)

        conn = get_db_connection()
        cursor = conn.cursor()

        # Check if the user owns the post
        cursor.execute("SELECT user_id FROM post WHERE post_id = %s", [post_id])
        post_owner = cursor.fetchone()

        if not post_owner or post_owner[0] != user_id:
            cursor.close()
            conn.close()
            return JsonResponse({'error': 'You are not authorized to edit this post'}, status=403)

        # Update the caption
        cursor.execute("UPDATE post SET caption = %s WHERE post_id = %s", (new_caption, post_id))
        conn.commit()

        cursor.close()
        conn.close()

        return JsonResponse({'success': 'Post updated successfully'})

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@login_required_json
def delete_post(request):
    try:
        # Validate method
        if request.method != 'DELETE':
            return JsonResponse({'error': 'Only DELETE method allowed'}, status=405)

        # Validate user session
        user_id = request.session.get('user_id')
        if not user_id:
            return JsonResponse({'error': 'User not authenticated'}, status=401)

        # Validate post_id in request body
        try:
            data = json.loads(request.body)
            post_id = data.get('post_id')
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

        if not post_id:
            return JsonResponse({'error': 'post_id is required'}, status=400)

        # Database connection
        conn = get_db_connection()
        cursor = conn.cursor()

        # Check if the post exists and is owned by the user
        cursor.execute("SELECT user_id FROM post WHERE post_id = %s", [post_id])
        post_owner = cursor.fetchone()

        if not post_owner:
            return JsonResponse({'error': 'Post not found'}, status=404)

        if post_owner[0] != user_id:
            return JsonResponse({'error': 'You are not authorized to delete this post'}, status=403)

        # Delete related likes
        cursor.execute("DELETE FROM likes WHERE post_id = %s", [post_id])

        # Delete related comments
        cursor.execute("DELETE FROM comment WHERE post_id = %s", [post_id])

        # Finally, delete the post
        cursor.execute("DELETE FROM post WHERE post_id = %s", [post_id])
        conn.commit()

        return JsonResponse({'success': 'Post deleted successfully'})

    except Exception as e:
        print(f"Error in delete_post: {e}")
        return JsonResponse({'error': 'Server error'}, status=500)

    finally:
        if 'cursor' in locals(): cursor.close()
        if 'conn' in locals(): conn.close()


@csrf_exempt
@login_required_json
def user_feed(request):
    try:
        if request.method != 'GET':
            return JsonResponse({'error': 'Only GET method allowed'}, status=405)

        user_id = request.session.get('user_id')

        if not user_id:
            return JsonResponse({'error': 'user_id is required'}, status=400)
        
        feed = []
        conn = get_db_connection()
        cursor = conn.cursor()

        # Fetch posts from friends and self
        cursor.execute(""" 
            SELECT 
                p.post_id, p.user_id, p.caption, p.image_url, p.timestamp,
                u.first_name, u.profile_picture
            FROM post p
            JOIN user u ON p.user_id = u.user_id
            WHERE p.user_id = %s OR p.user_id IN (
                SELECT 
                    CASE 
                        WHEN request = %s THEN acceptance 
                        WHEN acceptance = %s THEN request 
                    END
                FROM friends
                WHERE status = 'accepted'
            )
            ORDER BY p.timestamp DESC
        """, (user_id, user_id, user_id))
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
            """, (post_id,))
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

            # Add the post to the feed
            feed.append({
                'post_id': post_id,
                'user_id': author_id,
                'first_name': first_name,
                'profile_picture': f"/media/{profile_picture}" if profile_picture else "/assets/default_profile.png",
                'caption': caption,
                'image_url': f"/media/{image_url}" if image_url else None,
                'timestamp': timestamp.isoformat(),
                'like_count': like_count,
                'comment_count': comment_count,
                'comments': comments
            })

        cursor.close()
        conn.close()

        return JsonResponse({'posts': feed})

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@login_required_json
def user_posts(request, user_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Fetch posts for the given user
        cursor.execute("""
            SELECT post_id, caption, image_url, timestamp
            FROM post
            WHERE user_id = %s
            ORDER BY timestamp DESC
        """, (user_id,))
        posts = cursor.fetchall()

        # Format the image URLs
        for post in posts:
            if post["image_url"]:
                post["image_url"] = f"/media/{post['image_url']}"

        return JsonResponse({'posts': posts}, status=200)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()