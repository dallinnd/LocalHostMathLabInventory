from flask import Flask, request, jsonify, send_from_directory, Response
import os
import json
from functools import wraps

app = Flask(__name__, static_url_path='')
PORT = 8000
DATA_FILE = "database.json"

# --- CONFIGURATION ---
# These are the accounts that can log in.
# YOU CAN CHANGE THESE PASSWORDS HERE
USERS = {
    "admin": "AdminPassword123",
    "mathlabsec": "MathLabSecret456"
}

# --- SECURITY LOGIC ---
def check_auth(username, password):
    """Checks if username/password combination is valid."""
    return username in USERS and USERS[username] == password

def authenticate():
    """Sends a 401 response that forces the browser to pop up the Login box"""
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

# --- ROUTES ---

# 1. Serve the Frontend (Protected)
# This serves index.html when you go to http://[IP]:8000/
@app.route('/')
@requires_auth
def serve_index():
    return send_from_directory('.', 'index.html')

# This serves style.css, app.js, manifest.json, etc.
@app.route('/<path:path>')
@requires_auth
def serve_static(path):
    return send_from_directory('.', path)

# 2. API: Get Data (Protected)
# The PWA calls this to load the students/items
@app.route('/api/data', methods=['GET'])
@requires_auth
def get_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            data = json.load(f)
        return jsonify(data)
    else:
        # If no file exists yet, return empty lists
        return jsonify({"students": [], "items": []})

# 3. API: Save Data (Protected)
# The PWA calls this to save changes to your hard drive
@app.route('/api/data', methods=['POST'])
@requires_auth
def save_data():
    data = request.json
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)
    return jsonify({"status": "success"})

if __name__ == '__main__':
    # host='0.0.0.0' allows other computers on the network to connect
    print(f"Server running securely on port {PORT}")
    print(f"Access this computer's IP address at port {PORT}")
    app.run(host='0.0.0.0', port=PORT)
