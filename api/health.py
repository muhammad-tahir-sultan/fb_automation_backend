from flask import Flask

from lib._common import client, to_flask_response

app = Flask(__name__)


@app.route("/", methods=["GET"])
def health():
    try:
        client.server_info()
        return to_flask_response({"status": "ok"})
    except Exception as e:
        return to_flask_response({"status": "error", "message": str(e)}, status=500)
