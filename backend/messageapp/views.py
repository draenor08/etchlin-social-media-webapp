from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from backend.utils.auth import login_required_json
from backend.utils.db import get_db_connection

@csrf_exempt
@login_required_json
def send_message(request):
    if request.method == 'POST':
        sender_id = request.session.get('user_id')
        data = json.loads(request.body)
        receiver_id = data.get('receiver_id')
        text = data.get('text')

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO message (sender, receiver, text) VALUES (%s, %s, %s)", (sender_id, receiver_id, text))
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
        ORDER BY created_at
    """, (user_id, other_user_id, other_user_id, user_id))
    messages = cursor.fetchall()
    cursor.close()
    conn.close()
    return JsonResponse({'messages': messages})
