# File: userapp/views.py
import hashlib
import uuid
import mysql.connector
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.contrib.sessions.backends.db import SessionStore
import json

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