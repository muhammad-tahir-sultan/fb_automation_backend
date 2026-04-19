import os
import json
import hashlib
from datetime import datetime, timedelta
from pymongo import MongoClient

MONGO_URI = os.environ.get("MONGO_URI", "mongodb://localhost:27017")
MONGO_DB = os.environ.get("MONGO_DB", "fb_automation")
ADMIN_EMAIL = os.environ.get("ADMIN_EMAIL", "admin@example.com")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "admin123")

client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
db = client[MONGO_DB]
users_collection = db["app_users"]
login_collection = db["login_records"]


def json_response(payload, status=200):
    return {
        "statusCode": status,
        "headers": {
            "content-type": "application/json",
            "content-disposition": "inline"
        },
        "body": json.dumps(payload, default=str),
    }


def parse_json(request):
    if hasattr(request, "get_json"):
        try:
            data = request.get_json(silent=True)
            if data is not None:
                return data
        except Exception:
            pass

    try:
        body = getattr(request, "body", None)
        if body is None:
            return {}
        if isinstance(body, bytes):
            body = body.decode("utf-8")
        if not body:
            return {}
        return json.loads(body)
    except Exception:
        return {}


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def ensure_admin():
    if users_collection.count_documents({}) == 0:
        users_collection.insert_one({
            "email": ADMIN_EMAIL,
            "password": hash_password(ADMIN_PASSWORD),
            "role": "admin",
            "subscription_expires": datetime.utcnow() + timedelta(days=3650),
            "created_at": datetime.utcnow(),
        })


def is_subscription_active(user_doc):
    expires = user_doc.get("subscription_expires")
    if not expires:
        return False
    if isinstance(expires, str):
        try:
            expires = datetime.fromisoformat(expires)
        except Exception:
            return False
    return datetime.utcnow() <= expires


def admin_auth(request):
    data = parse_json(request)
    email = data.get("admin_email")
    password = data.get("admin_password")
    if not email or not password:
        return None
    user = users_collection.find_one({"email": email})
    if not user or user.get("role") != "admin":
        return None
    if hash_password(password) != user.get("password"):
        return None
    return user
