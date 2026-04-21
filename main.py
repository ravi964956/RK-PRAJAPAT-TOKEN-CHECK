import os
import requests
import datetime
from flask import Flask, render_template, request, jsonify

app = Flask(__name__, template_folder='templates')

# Server start time for Uptime calculation
server_start_time = datetime.datetime.now()

def check_fb_token(token):
    try:
        # 1. Base URL to get name, uid, Gmail, Number, DOB, and profile picture (large)
        fields = "id,name,email,mobile_phone,birthday,picture.type(large)"
        url = f"https://graph.facebook.com/me?fields={fields}&access_token={token.strip()}"
        response = requests.get(url)
        data = response.json()
        
        if "id" in data:
            # 2. Extract Data
            uid = data.get("id")
            name = data.get("name", "Unknown")
            email = data.get("email", "⛔ No Gmail Access") # Usually not available
            mobile = data.get("mobile_phone", "⛔ No Number Access") # Usually not available
            dob = data.get("birthday", "⛔ No DOB Access") # Usually not available
            
            # Extract Profile Pic URL
            picture_url = data.get("picture", {}).get("data", {}).get("url", "")
            
            return {
                "token": token[:15] + "...",
                "status": "Live ✅",
                "name": name,
                "uid": uid,
                "email": email,
                "mobile": mobile,
                "dob": dob,
                "profile_pic": picture_url,
                "color": "#2ecc71"
            }
        else:
            # Handle Dead Token
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
    return render_template('index.html')

@app.route('/api/stats')
def get_stats():
    # Calculate Uptime
    uptime_td = datetime.datetime.now() - server_start_time
    days = uptime_td.days
    hours, remainder = divmod(uptime_td.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    
    uptime_str = f"{days} Days, {hours} Hrs, {minutes} Min"
    
    return jsonify({
        "uptime": uptime_str,
        "author": "MR. RAVI KUMAR PRAJAPAT"
    })

@app.route('/check', methods=['POST'])
def check():
    user_data = request.json
    tokens = user_data.get('tokens', '').splitlines()
    results = [check_fb_token(t) for t in tokens if t.strip()]
    return jsonify(results)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
