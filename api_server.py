from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from calendar_tool import book_meeting, check_availability
from weather_tool import get_weather
from email_tool import send_reminder
import os

app = Flask(__name__)
CORS(app)

@app.route('/')
def serve_index():
    # Serve index.html from the current directory
    return send_file('index.html')

# ─── Calendar Endpoints ──────────────────────────────────────────────

@app.route('/api/book_meeting', methods=['POST'])
def handle_booking():
    data = request.json
    print(f"\n[API REQUEST] Booking {data.get('title')} at {data.get('date_time')}")
    result = book_meeting(date_time_iso=data.get('date_time'), name=data.get('guest_email'))
    print(f"[API RESPONSE] {result}")
    return jsonify({"result": result})

@app.route('/api/check_availability', methods=['POST'])
def handle_availability():
    data = request.json
    print(f"\n[API REQUEST] Checking availability for {data.get('date')}")
    result = check_availability(date_iso=data.get('date'))
    print(f"[API RESPONSE] {result}")
    return jsonify({"result": result})

# ─── Weather Endpoint ─────────────────────────────────────────────────

@app.route('/api/get_weather', methods=['POST'])
def handle_weather():
    data = request.json
    city = data.get('city', '')
    print(f"\n[API REQUEST] Weather for '{city}'")
    result = get_weather(city=city)
    print(f"[API RESPONSE] {result}")
    return jsonify({"result": result})

# ─── Email Reminder Endpoint ──────────────────────────────────────────

@app.route('/api/send_reminder', methods=['POST'])
def handle_reminder():
    data = request.json
    to_email = data.get('to_email', '')
    subject = data.get('subject', 'Reminder from VoiceNemo')
    body = data.get('body', '')
    print(f"\n[API REQUEST] Sending email to {to_email}: {subject}")
    result = send_reminder(to_email=to_email, subject=subject, body=body)
    print(f"[API RESPONSE] {result}")
    return jsonify({"result": result})

if __name__ == '__main__':
    print("Local API Bridge running on http://127.0.0.1:5000")
    print("   Calendar  -> /api/book_meeting, /api/check_availability")
    print("   Weather   -> /api/get_weather")
    print("   Email     -> /api/send_reminder")
    app.run(port=5000)