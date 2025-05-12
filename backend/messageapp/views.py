from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from utils.auth import login_required_json
from utils.db import get_db_connection
from datetime import datetime

@csrf_exempt
@login_required_json
def send_message(request):
    if request.method == 'POST':
        sender_id = request.session.get('user_id')
        data = json.loads(request.body)
        receiver_id = data.get('receiver_id')
        text = data.get('text')

        if not receiver_id or not text:
            return JsonResponse({'error': 'Missing receiver or message text'}, status=400)

        timestamp = datetime.now()

        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO message (sender_id, receiver_id, text, timestamp) VALUES (%s, %s, %s, %s)",
                (sender_id, receiver_id, text, timestamp)
            )
            conn.commit()
            message_number = cursor.lastrowid  # Get the ID of the inserted message

            # Fetch the inserted message to send back to the frontend
            cursor.execute("SELECT * FROM message WHERE message_number = %s", (message_number,))
            message = cursor.fetchone()
        except Exception as e:
            print("Database error in send_message:", e)
            return JsonResponse({'error': 'Database error'}, status=500)
        finally:
            cursor.close()
            conn.close()

        return JsonResponse(message, safe=False)


@login_required_json
def get_conversation(request, other_user_id):
    user_id = request.session.get('user_id')

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT message_number, sender_id, receiver_id, text, timestamp
            FROM message
            WHERE (sender_id = %s AND receiver_id = %s) OR (sender_id = %s AND receiver_id = %s)
            ORDER BY timestamp ASC
        """, (user_id, other_user_id, other_user_id, user_id))
        messages = cursor.fetchall()

        # Format timestamps for easier reading on the frontend
        for message in messages:
            if isinstance(message['timestamp'], datetime):
                message['timestamp'] = message['timestamp'].strftime('%Y-%m-%dT%H:%M:%SZ')

    except Exception as e:
        print("Database error in get_conversation:", e)
        return JsonResponse({'error': 'Database error'}, status=500)
    finally:
        cursor.close()
        conn.close()

    return JsonResponse({'messages': messages})

