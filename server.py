# server.py
from flask import Flask, request, jsonify, render_template, abort
import time
import threading

app = Flask(__name__)

# Simple in-memory store for events (also append to file)
events = []
events_lock = threading.Lock()
LOG_FILE = "remote_log.txt"

# Shared secret token (change to a long random string before use)
AUTH_TOKEN = "123456789"

def append_event(ev):
    with events_lock:
        events.append(ev)
        # keep file as permanent record
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(f"{ev['timestamp']} | {ev['window']} | {ev['text'].replace(chr(10),'\\\\n')}\n")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/ingest", methods=["POST"])
def ingest():
    # simple token auth
    token = request.headers.get("X-AUTH-TOKEN", "")
    if token != AUTH_TOKEN:
        abort(403)

    payload = request.get_json()
    if not payload:
        return "bad payload", 400

    # expected fields: timestamp, window, text
    ts = payload.get("timestamp", time.time())
    win = payload.get("window", "Unknown")
    text = payload.get("text", "")

    ev = {"timestamp": ts, "window": win, "text": text}
    append_event(ev)
    return jsonify({"status": "ok"}), 201

@app.route("/logs", methods=["GET"])
def logs():
    """
    Returns events after given 'since' param (float unix timestamp).
    """
    try:
        since = float(request.args.get("since", "0"))
    except:
        since = 0.0
    with events_lock:
        new = [e for e in events if float(e["timestamp"]) > since]
    return jsonify(new)

if __name__ == "__main__":
    # use host=0.0.0.0 if you want others on local network to connect
    app.run(host="0.0.0.0", port=5000, debug=True)
