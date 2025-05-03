import hashlib
import uuid

def hash_password(password):
    salt = uuid.uuid4().hex
    hashed = hashlib.sha256((password + salt).encode()).hexdigest()
    return f"{hashed}${salt}"

def check_password(password, hashed_with_salt):
    hashed, salt = hashed_with_salt.split("$")
    return hashed == hashlib.sha256((password + salt).encode()).hexdigest()
