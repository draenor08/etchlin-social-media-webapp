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

        created_at = datetime.now()

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO message (sender, receiver, text, created_at) VALUES (%s, %s, %s, %s)",
            (sender_id, receiver_id, text, created_at)
        )
        conn.commit()
        cursor.close()
        conn.close()

        return JsonResponse({'message': 'Message sent'})


@login_required_json
def get_conversation(request, other_user_id):
    user_id = request.session.get('user_id')

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT * FROM message
        WHERE (sender = %s AND receiver = %s) OR (sender = %s AND receiver = %s)
        ORDER BY created_at ASC
    """, (user_id, other_user_id, other_user_id, user_id))
    messages = cursor.fetchall()
    cursor.close()
    conn.close()

    return JsonResponse({'messages': messages})
