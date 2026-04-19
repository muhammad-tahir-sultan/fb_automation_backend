import json


def handler(request):
    """Root endpoint that displays available API endpoints."""
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
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
            "Content-Disposition": "inline"
        },
        "body": json.dumps(endpoints),
    }
