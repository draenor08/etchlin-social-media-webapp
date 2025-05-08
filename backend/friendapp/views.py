from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from utils.auth import login_required_json
from utils.db import get_db_connection
@csrf_exempt
def send_request(request):
    if request.method == 'POST':
        sender_id = request.session.get('user_id')
        if not sender_id:
            return JsonResponse({'error': 'Not logged in'}, status=401)

        data = json.loads(request.body)
        receiver_id = data.get('receiver_id')

        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO friends (request, acceptance, status) VALUES (%s, %s, 'pending')", (sender_id, receiver_id))
            conn.commit()
            return JsonResponse({'message': 'Friend request sent'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
        finally:
            cursor.close()
            conn.close()

@csrf_exempt
def respond_request(request):
    if request.method == 'POST':
        user_id = request.session.get('user_id')
        data = json.loads(request.body)
        requester_id = data.get('requester_id')
        action = data.get('action')  # 'accept' or 'reject'
        if requester_id == user_id:
            return JsonResponse({'error': 'Cannot send friend request to yourself'}, status=400)


        status = 'accepted' if action == 'accept' else 'rejected'

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE friends SET status = %s WHERE request = %s AND acceptance = %s", (status, requester_id, user_id))
        conn.commit()
        cursor.close()
        conn.close()

        return JsonResponse({'message': f'Request {status}'})

@login_required_json
def get_friends(request):
    user_id = request.session.get('user_id')
    
    if not user_id:
        return JsonResponse({'error': 'Unauthorized'}, status=401)
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT u.user_id, u.first_name, u.last_name, u.profile_picture_path
            FROM friends f 
            JOIN user u ON (f.request = u.user_id OR f.acceptance = u.user_id)
            WHERE (f.request = %s OR f.acceptance = %s) 
            AND f.status = 'accepted' 
            AND u.user_id != %s
        """, (user_id, user_id, user_id))
        friends = cursor.fetchall()
    except Exception as e:
        print("Database Error:", e)
        return JsonResponse({'error': 'Database error'}, status=500)
    finally:
        cursor.close()
        conn.close()

    return JsonResponse({'friends': friends})