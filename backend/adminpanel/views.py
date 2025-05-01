from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .db_interface import get_flagged_posts, resolve_flag

def flagged_posts_view(request):
    # Assume admin only
    posts = get_flagged_posts()
    return JsonResponse({"flagged_posts": posts})

@csrf_exempt
def resolve_flag_view(request):
    if request.method == "POST":
        data = json.loads(request.body)
        success = resolve_flag(data['post_id'], data['action'])  # "delete" or "ignore"
        return JsonResponse({"message": "Resolved"} if success else {"error": "Failed"})

