from lib._common import json_response, parse_json, users_collection, hash_password, ensure_admin
from datetime import datetime, timedelta


def handler(request):
    ensure_admin()
    method = getattr(request, "method", "GET")

    if method == "GET":
        users = []
        for doc in users_collection.find().sort("email", 1):
            users.append({
                "email": doc.get("email"),
                "role": doc.get("role"),
                "subscription_expires": doc.get("subscription_expires"),
            })
        return json_response({"success": True, "users": users})

    if method == "POST":
        data = parse_json(request)
        admin = ensure_admin()  # ensure default admin exists
        admin_user = None
        if data.get("admin_email") and data.get("admin_password"):
            admin_user = users_collection.find_one({"email": data.get("admin_email")})
        if not admin_user or admin_user.get("role") != "admin" or hash_password(data.get("admin_password", "")) != admin_user.get("password"):
            return json_response({"success": False, "message": "Admin authentication required."}, status=401)

        email = data.get("email")
        password = data.get("password")
        role = data.get("role", "user")
        months = int(data.get("months", 1))

        if not email or not password:
            return json_response({"success": False, "message": "Email and password required."}, status=400)

        if users_collection.find_one({"email": email}):
            return json_response({"success": False, "message": "User already exists."}, status=409)

        expires = datetime.utcnow() + timedelta(days=30 * months)
        users_collection.insert_one({
            "email": email,
            "password": hash_password(password),
            "role": role,
            "subscription_expires": expires,
            "created_at": datetime.utcnow(),
        })

        return json_response({"success": True, "message": "User created.", "subscription_expires": expires}, status=201)

    return json_response({"success": False, "message": "Method not allowed."}, status=405)
