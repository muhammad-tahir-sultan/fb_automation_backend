from lib._common import json_response, parse_json, users_collection, hash_password, is_subscription_active, ensure_admin


def handler(request):
    ensure_admin()
    data = parse_json(request)
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return json_response({"success": False, "message": "Email and password required."}, status=400)

    user = users_collection.find_one({"email": email})
    if not user:
        return json_response({"success": False, "message": "User not found."}, status=404)

    if hash_password(password) != user.get("password"):
        return json_response({"success": False, "message": "Invalid credentials."}, status=401)

    if user.get("role") != "admin" and not is_subscription_active(user):
        return json_response({"success": False, "message": "Subscription expired."}, status=403)

    return json_response({
        "success": True,
        "email": user.get("email"),
        "role": user.get("role"),
        "subscription_expires": user.get("subscription_expires"),
    })
