from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from utils.auth import login_required_json
from utils.db import get_db_connection

@csrf_exempt
@login_required_json
def send_request(request):
    if request.method == 'POST':
        sender_id = request.session.get('user_id')
        if not sender_id:
            return JsonResponse({'error': 'Not logged in'}, status=401)

        try:
            data = json.loads(request.body)
            receiver_id = data.get('receiver_id')
            if not receiver_id:
                return JsonResponse({'error': 'Receiver ID required'}, status=400)

            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO friends (request, acceptance, status) 
                VALUES (%s, %s, 'pending')
            """, (sender_id, receiver_id))
            conn.commit()

            return JsonResponse({'message': 'Friend request sent'}, status=201)
        except Exception as e:
            print("Error in send_request:", e)
            return JsonResponse({'error': 'Database error'}, status=500)
        finally:
            cursor.close()
            conn.close()

    return JsonResponse({'error': 'Invalid request method'}, status=405)


@csrf_exempt
def respond_request(request):
    if request.method == 'POST':
        user_id = request.session.get('user_id')
        data = json.loads(request.body)
        requester_id = data.get('requester_id')
        action = data.get('action')
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
    
@csrf_exempt
@login_required_json
def get_requests(request):
    try:
        user_id = request.session.get('user_id')
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT u.user_id, u.first_name, u.last_name, u.profile_picture
            FROM friends f
            JOIN user u ON f.request = u.user_id
            WHERE f.acceptance = %s AND f.status = 'pending'
        """, (user_id,))
        requests = cursor.fetchall()
    except Exception as e:
        print("Database error in get_requests:", e)
        return JsonResponse({'error': 'Database error'}, status=500)
    finally:
        cursor.close()
        conn.close()

    return JsonResponse({'requests': requests})

@login_required_json
def get_friends(request):
    user_id = request.session.get('user_id')
    
    if not user_id:
        return JsonResponse({'error': 'Unauthorized'}, status=401)
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT u.user_id, u.first_name, u.last_name, u.profile_picture
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

@csrf_exempt 
@login_required_json
def remove_friend(request):
    if request.method == 'POST':
        user_id = request.session.get('user_id')
        data = json.loads(request.body)
        receiver_id = data.get('receiver_id')

        if not receiver_id or receiver_id == user_id:
            return JsonResponse({'error': 'Invalid receiver ID'}, status=400)

        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("""
                DELETE FROM friends 
                WHERE (request = %s AND acceptance = %s) 
                OR (request = %s AND acceptance = %s)
            """, (user_id, receiver_id, receiver_id, user_id))
            conn.commit()

            return JsonResponse({'message': 'Friend removed successfully'})
        except Exception as e:
            print(f"Error in remove_friend: {e}")
            return JsonResponse({'error': 'Server error'}, status=500)
        finally:
            cursor.close()
            conn.close()

    return JsonResponse({'error': 'Invalid request method'}, status=405)


@csrf_exempt
@login_required_json
def friend_status(request, user_id):
    current_user_id = request.session.get('user_id')
    if not current_user_id or current_user_id == user_id:
        return JsonResponse({'status': 'self'}, status=400)

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT status FROM friends 
            WHERE (request = %s AND acceptance = %s) 
            OR (request = %s AND acceptance = %s)
        """, (current_user_id, user_id, user_id, current_user_id))
        result = cursor.fetchone()
        status = result[0] if result else 'not_friends'
    except Exception as e:
        print("Database error in friend_status:", e)
        return JsonResponse({'error': 'Database error'}, status=500)
    finally:
        cursor.close()
        conn.close()

    return JsonResponse({'status': status})

@login_required_json
def friend_count(request, user_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT COUNT(*) FROM friends 
            WHERE (request = %s OR acceptance = %s) 
            AND status = 'accepted'
        """, (user_id, user_id))
        count = cursor.fetchone()[0]
    except Exception as e:
        print("Database error in friend_count:", e)
        return JsonResponse({'error': 'Database error'}, status=500)
    finally:
        cursor.close()
        conn.close()

    return JsonResponse({'count': count})
