from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
import os

app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)  # Enable CORS so frontend can access backend from GitHub Pages

# Multilingual lesson data
lessons = {
    "whatsapp": {
        "en": "1. Open WhatsApp\n2. Tap contact\n3. Type your message\n4. Press Send.",
        "hi": "1. WhatsApp खोलें\n2. संपर्क चुनें\n3. अपना संदेश लिखें\n4. भेजें दबाएं।",
        "bn": "1. WhatsApp খুলুন\n2. কনট্যাক্ট চাপুন\n3. মেসেজ লিখুন\n4. সেন্ড করুন।"
    },
    "call": {
        "en": "1. Open the Phone app\n2. Dial or select contact\n3. Tap the call button.",
        "hi": "1. फ़ोन ऐप खोलें\n2. नंबर डायल करें या संपर्क चुनें\n3. कॉल बटन दबाएं।",
        "bn": "1. ফোন অ্যাপ খুলুন\n2. নম্বর ডায়াল করুন বা কনট্যাক্ট বাছুন\n3. কল বোতাম চাপুন।"
    },
    "upi": {
        "en": "1. Open UPI app\n2. Scan QR or enter number\n3. Enter amount\n4. Enter PIN.",
        "hi": "1. UPI ऐप खोलें\n2. QR स्कैन करें या नंबर दर्ज करें\n3. राशि दर्ज करें\n4. पिन दर्ज करें।",
        "bn": "1. UPI অ্যাপ খুলুন\n2. QR স্ক্যান করুন অথবা নম্বর দিন\n3. পরিমাণ লিখুন\n4. পিন দিন।"
    },
    "safety": {
        "en": "1. Never share OTP\n2. Don't click unknown links\n3. Use trusted apps.",
        "hi": "1. OTP कभी साझा न करें\n2. अज्ञात लिंक पर क्लिक न करें\n3. केवल विश्वसनीय ऐप का उपयोग करें।",
        "bn": "1. OTP কখনো শেয়ার করবেন না\n2. অচেনা লিংকে ক্লিক করবেন না\n3. বিশ্বস্ত অ্যাপ ব্যবহার করুন।"
    }
}

# Routes
@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/lesson/<lesson_type>/<lang>')
def get_lesson(lesson_type, lang):
    lesson = lessons.get(lesson_type.lower())
    if lesson:
        content = lesson.get(lang.lower())
        if content:
            return jsonify({"content": content})
    return jsonify({"error": "Lesson not found"}), 404

@app.route('/video/<filename>')
def get_video(filename):
    return send_from_directory('video', filename)

# Run the app
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
