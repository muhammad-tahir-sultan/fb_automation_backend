from flask import Flask, request
from datetime import datetime, timedelta

from lib._common import parse_json, users_collection, hash_password, ensure_admin, to_flask_response

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def users():
    ensure_admin()
    method = request.method

    if method == "GET":
        users = []
        for doc in users_collection.find().sort("email", 1):
            users.append({
                "email": doc.get("email"),
                "role": doc.get("role"),
                "subscription_expires": doc.get("subscription_expires"),
            })
        return to_flask_response({"success": True, "users": users})

    if method == "POST":
        data = parse_json(request)
        ensure_admin()
        admin_user = None
        if data.get("admin_email") and data.get("admin_password"):
            admin_user = users_collection.find_one({"email": data.get("admin_email")})
        if not admin_user or admin_user.get("role") != "admin" or hash_password(data.get("admin_password", "")) != admin_user.get("password"):
            return to_flask_response({"success": False, "message": "Admin authentication required."}, status=401)

        email = data.get("email")
        password = data.get("password")
        role = data.get("role", "user")
        months = int(data.get("months", 1))

        if not email or not password:
            return to_flask_response({"success": False, "message": "Email and password required."}, status=400)

        if users_collection.find_one({"email": email}):
            return to_flask_response({"success": False, "message": "User already exists."}, status=409)

        expires = datetime.utcnow() + timedelta(days=30 * months)
        users_collection.insert_one({
            "email": email,
            "password": hash_password(password),
            "role": role,
            "subscription_expires": expires,
            "created_at": datetime.utcnow(),
        })

        return to_flask_response({"success": True, "message": "User created.", "subscription_expires": expires}, status=201)

    return to_flask_response({"success": False, "message": "Method not allowed."}, status=405)
