import hashlib
import uuid
import json
import os
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import mysql.connector

# --- DB CONFIG ---
DB_CONFIG = {
    'host': 'localhost',
    'user': settings.DATABASES['default']['USER'],
    'password': settings.DATABASES['default']['PASSWORD'],
    'database': settings.DATABASES['default']['NAME'],
}

def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)

# --- PASSWORD UTILS ---
def hash_password(password):
    salt = uuid.uuid4().hex
    hashed = hashlib.sha256((password + salt).encode()).hexdigest()
    return f"{hashed}${salt}"

def check_password(password, hashed_with_salt):
    hashed, salt = hashed_with_salt.split("$")
    return hashed == hashlib.sha256((password + salt).encode()).hexdigest()

# --- REGISTER ---
@csrf_exempt
def register_user(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST method allowed'}, status=405)

    try:
        data = json.loads(request.body)
        email = data.get('email')
        password = data.get('password')
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        date_of_birth = data.get('date_of_birth')
        bio = data.get('bio', '')

        if not all([email, password, first_name, last_name, date_of_birth]):
            return JsonResponse({'error': 'Missing required fields'}, status=400)

        hashed_password = hash_password(password)

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT user_id FROM user WHERE email = %s", (email,))
        if cursor.fetchone():
            return JsonResponse({'error': 'Email already exists'}, status=409)

        cursor.execute("""
            INSERT INTO user (email, password, first_name, last_name, date_of_birth, bio)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (email, hashed_password, first_name, last_name, date_of_birth, bio))

        conn.commit()
        return JsonResponse({'message': 'User registered successfully'}, status=201)

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

# --- LOGIN ---
@csrf_exempt
def login(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST allowed'}, status=405)

    try:
        data = json.loads(request.body)
        email = data.get('email')
        password = data.get('password')

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT user_id, password FROM user WHERE email=%s", (email,))
        user = cursor.fetchone()

        if user and check_password(password, user['password']):
            request.session['user_id'] = user['user_id']
            return JsonResponse({'message': 'Login successful'})
        else:
            return JsonResponse({'error': 'Invalid credentials'}, status=401)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

# --- UPLOAD PROFILE PIC ---
@csrf_exempt
def upload_profile_picture(request, user_id):
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST method allowed'}, status=405)

    image = request.FILES.get('image')

    if not user_id or not image:
        return JsonResponse({'error': 'Missing user_id or image'}, status=400)

    try:
        # Save image
        image_name = f"profile_{user_id}_{uuid.uuid4().hex}.jpg"
        save_path = os.path.join(settings.MEDIA_ROOT, 'profile_pics', image_name)
        os.makedirs(os.path.dirname(save_path), exist_ok=True)

        with open(save_path, 'wb+') as f:
            for chunk in image.chunks():
                f.write(chunk)

        relative_path = f"media/profile_pics/{image_name}"

        # Update DB
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE user SET profile_picture = %s WHERE user_id = %s
        """, (relative_path, user_id))
        conn.commit()

        return JsonResponse({
            'message': 'Profile picture uploaded successfully',
            'image_url': request.build_absolute_uri('/' + relative_path)
            })

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

# --- GET PROFILE ---
@csrf_exempt
def get_user_profile(request, user_id):
    if request.method != 'GET':
        return JsonResponse({'error': 'Only GET allowed'}, status=405)

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
