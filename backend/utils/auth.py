import hashlib
import uuid
from django.http import JsonResponse
from functools import wraps

def hash_password(password):
    salt = uuid.uuid4().hex
    hashed = hashlib.sha256((password + salt).encode()).hexdigest()
    return f"{hashed}${salt}"

def check_password(password, hashed_with_salt):
    hashed, salt = hashed_with_salt.split("$")
    return hashed == hashlib.sha256((password + salt).encode()).hexdigest()

def login_required_json(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.session.get('user_id'):
            return JsonResponse({'error': 'Authentication required'}, status=401)
        return view_func(request, *args, **kwargs)
    return wrapper
