import os
import requests
from flask import Flask, render_template, request, jsonify

# Template folder configuration
app = Flask(__name__, template_folder='templates')

def check_fb_token(token):
    try:
        # Facebook Graph API to verify token
        url = f"https://graph.facebook.com/me?access_token={token.strip()}"
        response = requests.get(url)
        data = response.json()
        
        if "id" in data:
            return {
                "token": token[:15] + "...",
                "status": "Live ✅",
                "name": data.get("name", "Unknown"),
                "id": data.get("id"),
                "color": "#2ecc71"
            }
        else:
            error_msg = data.get("error", {}).get("message", "Invalid Token")
            return {
                "token": token[:15] + "...",
                "status": "Dead ❌",
                "message": error_msg,
                "color": "#e74c3c"
            }
    except Exception as e:
        return {"token": "Error", "status": "Error ⚠️", "message": str(e), "color": "#f1c40f"}

@app.route('/')
def index():
    # Diagnostic check for templates
    return render_template('index.html')

@app.route('/check', methods=['POST'])
def check():
    user_data = request.json
    tokens = user_data.get('tokens', '').splitlines()
    results = [check_fb_token(t) for t in tokens if t.strip()]
    return jsonify(results)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
  
