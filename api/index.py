import json
from flask import Flask

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    endpoints = {
        "status": "ok",
        "name": "Facebook Login Automation API",
        "version": "1.0.0",
        "endpoints": {
            "GET /api/health": "Check MongoDB connection status",
            "POST /api/login": "Authenticate user and record login",
            "POST /api/users": "Create or list users",
            "GET /api/record": "Get login records",
            "POST /api/renew": "Renew user subscription",
        }
    }
    return (
        json.dumps(endpoints),
        200,
        {
            "Content-Type": "application/json",
            "Content-Disposition": "inline",
        },
    )
