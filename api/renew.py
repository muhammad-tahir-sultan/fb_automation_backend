from ._common import json_response, parse_json, users_collection, hash_password, ensure_admin
from datetime import datetime, timedelta


def handler(request):
    ensure_admin()
    data = parse_json(request)
    admin_user = None
    if data.get("admin_email") and data.get("admin_password"):
        admin_user = users_collection.find_one({"email": data.get("admin_email")})
    if not admin_user or admin_user.get("role") != "admin" or hash_password(data.get("admin_password", "")) != admin_user.get("password"):
        return json_response({"success": False, "message": "Admin authentication required."}, status=401)

    email = data.get("email")
    months = int(data.get("months", 1))

    if not email:
        return json_response({"success": False, "message": "Email required."}, status=400)

    user = users_collection.find_one({"email": email})
    if not user:
        return json_response({"success": False, "message": "User not found."}, status=404)

    expiry = user.get("subscription_expires")
    if isinstance(expiry, str):
        try:
            expiry = datetime.fromisoformat(expiry)
        except Exception:
            expiry = None

    if not expiry or expiry < datetime.utcnow():
        expiry = datetime.utcnow()

    new_expiry = expiry + timedelta(days=30 * months)
    users_collection.update_one({"email": email}, {"$set": {"subscription_expires": new_expiry}})

    return json_response({"success": True, "message": "Subscription renewed.", "subscription_expires": new_expiry})
