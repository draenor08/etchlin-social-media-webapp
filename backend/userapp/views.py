# File: userapp/views.py
from datetime import timezone
import hashlib
import uuid
from django.db import connection
import mysql.connector
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.contrib.sessions.backends.db import SessionStore
import json
import os

DB_CONFIG = {
    'host': 'localhost',
    'user': settings.DATABASES['default']['USER'],
    'password': settings.DATABASES['default']['PASSWORD'],
    'database': settings.DATABASES['default']['NAME'],
}

def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)

def hash_password(password):
    salt = uuid.uuid4().hex
    hashed = hashlib.sha256((password + salt).encode()).hexdigest()
    return f"{hashed}${salt}"

def check_password(password, hashed_with_salt):
    hashed, salt = hashed_with_salt.split("$")
    return hashed == hashlib.sha256((password + salt).encode()).hexdigest()

@csrf_exempt
def register(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST allowed'}, status=405)
    
    data = json.loads(request.body)
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return JsonResponse({'error': 'Missing username or password'}, status=400)

    hashed_password = hash_password(password)
    
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_password))
        conn.commit()
        return JsonResponse({'message': 'User registered successfully'})
    except mysql.connector.Error as err:
        return JsonResponse({'error': str(err)}, status=500)
    finally:
        cursor.close()
        conn.close()

@csrf_exempt
def login(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST allowed'}, status=405)

    data = json.loads(request.body)
    username = data.get('username')
    password = data.get('password')

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, password FROM users WHERE username=%s", (username,))
    user = cursor.fetchone()

    if user and check_password(password, user['password']):
        request.session['user_id'] = user['id']
        return JsonResponse({'message': 'Login successful'})
    else:
        return JsonResponse({'error': 'Invalid credentials'}, status=401)
    
@csrf_exempt
def upload_profile_picture(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        image = request.FILES.get('image')

        if not user_id or not image:
            return JsonResponse({'error': 'Missing user_id or image'}, status=400)

        # Save image
        image_name = f"profile_{user_id}_{timezone.now().timestamp()}.jpg"
        save_path = os.path.join(settings.MEDIA_ROOT, 'profile_pics', image_name)
        os.makedirs(os.path.dirname(save_path), exist_ok=True)

        with open(save_path, 'wb+') as f:
            for chunk in image.chunks():
                f.write(chunk)

        relative_path = f"media/profile_pics/{image_name}"

        # Update DB
        with connection.cursor() as cursor:
            cursor.execute("""
                UPDATE user
                SET profile_picture = %s
                WHERE user_id = %s
            """, [relative_path, user_id])

        return JsonResponse({'message': 'Profile picture uploaded successfully', 'path': relative_path})

    return JsonResponse({'error': 'Only POST method allowed'}, status=405)

@csrf_exempt
def get_user_profile(request, user_id):
    if request.method == 'GET':
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)

            query = """
                SELECT user_id, first_name, last_name, bio, profile_picture_url
                FROM user
                WHERE user_id = %s
            """
            cursor.execute(query, (user_id,))
            user = cursor.fetchone()

            if user:
                return JsonResponse(user)
            else:
                return JsonResponse({'error': 'User not found'}, status=404)

        except mysql.connector.Error as err:
            return JsonResponse({'error': str(err)}, status=500)
        finally:
            cursor.close()
            conn.close()

    return JsonResponse({'error': 'Only GET allowed'}, status=405)
