import os
import uuid
import json
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import redirect
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.views.decorators.csrf import csrf_exempt

from backend.utils.auth import hash_password, check_password, login_required_json
from backend.utils.db import get_db_connection

# REGISTER USER
@csrf_exempt
def register_user(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data['email']
            password = hash_password(data['password'])
            first_name = data['first_name']
            last_name = data['last_name']

            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO user (email, password, first_name, last_name) VALUES (%s, %s, %s, %s)",
                           (email, password, first_name, last_name))
            conn.commit()
            return JsonResponse({'message': 'User registered successfully'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'conn' in locals():
                conn.close()
    return JsonResponse({'error': 'Invalid method'}, status=405)

# LOGIN USER
@csrf_exempt
def login_user(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data['email']
            password = data['password']

            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM user WHERE email = %s", (email,))
            user = cursor.fetchone()

            if user and check_password(password, user['password']):
                request.session['user_id'] = user['user_id']
                return JsonResponse({'message': 'Login successful'})
            return JsonResponse({'error': 'Invalid credentials'}, status=401)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'conn' in locals():
                conn.close()
    return JsonResponse({'error': 'Invalid method'}, status=405)

# LOGOUT
@csrf_exempt
def logout_user(request):
    request.session.flush()
    return JsonResponse({'message': 'Logged out successfully'})

# GET OWN PROFILE
@csrf_exempt
@login_required_json
def get_own_profile(request):
    user_id = request.session.get('user_id')
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT user_id, first_name, last_name, bio, profile_picture
            FROM user WHERE user_id = %s
        """, (user_id,))
        user = cursor.fetchone()

        if user:
            return JsonResponse(user)
        else:
            return JsonResponse({'error': 'User not found'}, status=404)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()
            
# UPDATE PROFILE PICTURE
@csrf_exempt
@login_required_json
def update_profile_picture(request):
    if request.method == 'POST' and request.FILES.get('profile_picture'):
        user_id = request.session.get('user_id')
        profile_pic = request.FILES['profile_picture']
        file_ext = os.path.splitext(profile_pic.name)[-1]
        unique_filename = f"profile_{uuid.uuid4().hex}{file_ext}"
        save_path = os.path.join('profile_pictures', unique_filename)

        try:
            full_path = default_storage.save(save_path, ContentFile(profile_pic.read()))
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("UPDATE user SET profile_picture = %s WHERE user_id = %s", (full_path, user_id))
            conn.commit()
            return JsonResponse({'message': 'Profile picture updated', 'path': full_path})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
        finally:
            if 'cursor' in locals(): cursor.close()
            if 'conn' in locals(): conn.close()
    return JsonResponse({'error': 'Invalid request'}, status=400)

from django.http import JsonResponse
from utils.auth import login_required_json
from utils.db import get_db_connection

@login_required_json
def post_feed(request):
    user_id = request.session.get('user_id')
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        # Fetch user's and friends' posts, most recent first
        cursor.execute("""
            SELECT p.post_id, p.caption, p.image_path, p.timestamp, u.username
            FROM post p
            JOIN user u ON p.user_id = u.user_id
            WHERE p.user_id = %s OR p.user_id IN (
                SELECT CASE
                    WHEN f.request = %s THEN f.acceptance
                    WHEN f.acceptance = %s THEN f.request
                END
                FROM friends f
                WHERE (f.request = %s OR f.acceptance = %s) AND f.status = 'accepted'
            )
            ORDER BY p.timestamp DESC
        """, (user_id, user_id, user_id, user_id, user_id))
        posts = cursor.fetchall()
        return JsonResponse({'posts': posts})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    finally:
        cursor.close()
        conn.close()
