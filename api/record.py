from lib._common import json_response, parse_json, login_collection
from datetime import datetime


def handler(request):
    data = parse_json(request)
    if not data.get("email") or not data.get("status"):
        return json_response({"success": False, "message": "Email and status required."}, status=400)

    login_collection.insert_one({
        "timestamp": datetime.utcnow(),
        "email": data.get("email"),
        "status": data.get("status"),
        "details": data.get("details", ""),
        "proxy_enabled": bool(data.get("proxy_enabled", False)),
    })

    return json_response({"success": True})
