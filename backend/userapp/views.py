import os
import uuid
import json
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import redirect
from utils.db import get_db_connection
from django.core.files.base import ContentFile
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from utils.auth import hash_password, check_password, login_required_json


def get_user_info(request):
    user_id = request.session.get('user_id')

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute(
            "SELECT user_id, first_name, last_name, profile_picture FROM user WHERE user_id = %s",
            (user_id,)
        )
        user = cursor.fetchone()
    except Exception as e:
        print("Database error in get_user_info:", e)
        return JsonResponse({'error': 'Database error'}, status=500)
    finally:
        cursor.close()
        conn.close()

    return JsonResponse({'user': user})

def check_auth(request):
    if request.session.get('user_id'):
        return JsonResponse({'status': 'authenticated'})
    return JsonResponse({'status': 'unauthenticated'}, status=401)

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
            date_of_birth = data['dob']  

            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO user (email, password, first_name, last_name, date_of_birth)
                VALUES (%s, %s, %s, %s, %s)
            """, (email, password, first_name, last_name, date_of_birth))
            
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
                cursor.close()
                conn.close()
                return JsonResponse({'message': 'Login successful'})
            return JsonResponse({'error': 'Invalid credentials'}, status=401)

        except Exception as e:
            print(e)
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

@csrf_exempt
@login_required_json
def get_profile(request, user_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Fetch profile data
        cursor.execute("""
            SELECT user_id, first_name, last_name, email, bio, profile_picture, date_of_birth
            FROM user WHERE user_id = %s
        """, (user_id,))
        user = cursor.fetchone()

        # Fetch user posts
        cursor.execute("""
            SELECT post_id, caption, image_url, timestamp
            FROM post WHERE user_id = %s
            ORDER BY timestamp DESC
        """, (user_id,))
        posts = cursor.fetchall()

        if user:
            return JsonResponse({
                'user': user,
                'posts': posts
            })
        else:
            return JsonResponse({'error': 'User not found'}, status=404)

    except Exception as e:
        print("Database error in get_profile:", e)
        return JsonResponse({'error': 'Database error'}, status=500)
    finally:
        if 'cursor' in locals(): cursor.close()
        if 'conn' in locals(): conn.close()


@csrf_exempt
@login_required_json
def upload_profile_picture(request):
    if request.method == 'POST' and request.FILES.get('profile_picture'):
        user_id = request.session.get('user_id')
        profile_pic = request.FILES['profile_picture']
        file_ext = os.path.splitext(profile_pic.name)[-1]
        unique_filename = f"person_{uuid.uuid4().hex}{file_ext}"
        save_path = os.path.join('person', unique_filename)

        try:
            # Save file
            full_path = default_storage.save(save_path, ContentFile(profile_pic.read()))

            # Update DB
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("UPDATE user SET profile_picture = %s WHERE user_id = %s", (save_path, user_id))
            conn.commit()
            return JsonResponse({'message': 'Profile picture updated', 'path': save_path})
        
        except Exception as e:
            print("Database error in upload_profile_picture:", e)
            return JsonResponse({'error': 'Database error'}, status=500)

        finally:
            if 'cursor' in locals(): cursor.close()
            if 'conn' in locals(): conn.close()

    return JsonResponse({'error': 'Invalid request'}, status=400)

@csrf_exempt
@login_required_json
def update_bio(request):
    if request.method == 'POST':
        user_id = request.session.get('user_id')
        try:
            data = json.loads(request.body)
            new_bio = data.get('bio', '').strip()

            if len(new_bio) > 250:
                return JsonResponse({'error': 'Bio is too long (max 250 characters)'}, status=400)

            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("UPDATE user SET bio = %s WHERE user_id = %s", (new_bio, user_id))
            conn.commit()
            return JsonResponse({'message': 'Bio updated successfully'})

        except Exception as e:
            print("Database error in update_bio:", e)
            return JsonResponse({'error': 'Database error'}, status=500)

        finally:
            if 'cursor' in locals(): cursor.close()
            if 'conn' in locals(): conn.close()

    return JsonResponse({'error': 'Invalid request'}, status=400)

@csrf_exempt
@login_required_json
def search_users(request):
    try:
        query = request.GET.get('q', '').strip()
        if not query:
            return JsonResponse([], safe=False)

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Split the query to handle full name searches
        terms = query.split()
        if len(terms) == 1:
            # Search by first or last name
            cursor.execute("""
                SELECT user_id, first_name, last_name, profile_picture 
                FROM user 
                WHERE first_name LIKE %s OR last_name LIKE %s
            """, (f"%{terms[0]}%", f"%{terms[0]}%"))
        else:
            # Search by full name
            cursor.execute("""
                SELECT user_id, first_name, last_name, profile_picture 
                FROM user 
                WHERE (first_name LIKE %s AND last_name LIKE %s) 
                OR (first_name LIKE %s AND last_name LIKE %s)
            """, (f"%{terms[0]}%", f"%{terms[1]}%", f"%{terms[1]}%", f"%{terms[0]}%"))

        users = cursor.fetchall()
        cursor.close()
        conn.close()

        return JsonResponse(users, safe=False)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)