from flask import Flask, request
from datetime import datetime

from lib._common import parse_json, login_collection, to_flask_response

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def record():
    data = parse_json(request)
    if request.method == "GET":
        records = []
        for doc in login_collection.find().sort("timestamp", -1):
            records.append({
                "timestamp": doc.get("timestamp"),
                "email": doc.get("email"),
                "status": doc.get("status"),
                "details": doc.get("details", ""),
                "proxy_enabled": bool(doc.get("proxy_enabled", False)),
            })
        return to_flask_response({"success": True, "records": records})

    if not data.get("email") or not data.get("status"):
        return to_flask_response({"success": False, "message": "Email and status required."}, status=400)

    login_collection.insert_one({
        "timestamp": datetime.utcnow(),
        "email": data.get("email"),
        "status": data.get("status"),
        "details": data.get("details", ""),
        "proxy_enabled": bool(data.get("proxy_enabled", False)),
    })

    return to_flask_response({"success": True})
