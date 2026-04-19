from ._common import json_response, client


def handler(request):
    try:
        client.server_info()
        return json_response({"status": "ok"})
    except Exception as e:
        return json_response({"status": "error", "message": str(e)}, status=500)
