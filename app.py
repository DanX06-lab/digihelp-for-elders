from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
import os

app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)  # ← ENABLE CORS here ✅

lessons = {
    "whatsapp": "1. Open WhatsApp\n2. Tap contact\n3. Type your message\n4. Press Send.",
    "call": "1. Open the Phone app\n2. Dial or select contact\n3. Tap the call button.",
    "upi": "1. Open UPI app\n2. Scan QR or enter number\n3. Enter amount\n4. Enter PIN.",
    "safety": "1. Never share OTP\n2. Don't click on unknown links\n3. Use trusted apps."
}

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/lesson/<lesson_type>')
def get_lesson(lesson_type):
    content = lessons.get(lesson_type.lower())
    if content:
        return jsonify({"content": content})
    return jsonify({"error": "Lesson not found"}), 404

@app.route('/video/<filename>')
def get_video(filename):
    return send_from_directory('video', filename)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
