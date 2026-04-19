from ._common import json_response


def handler(request):
    """Root endpoint that displays available API endpoints."""
    endpoints = {
        "status": "ok",
        "api": "Facebook Login Automation API",
        "endpoints": {
            "GET /api/health": "Check MongoDB connection status",
            "POST /api/login": "Authenticate user and record login",
            "POST /api/users": "Create or list users",
            "GET /api/record": "Get login records",
            "POST /api/renew": "Renew user subscription",
        },
        "documentation": "https://github.com/yourusername/fb_automation"
    }
    return json_response(endpoints)
