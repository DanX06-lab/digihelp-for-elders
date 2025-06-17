from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import os
import json

app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)

LESSON_FILE = "lessons.json"

# Load lessons from JSON file
def load_lessons():
    try:
        with open(LESSON_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

# Save lessons to JSON file
def save_lessons(data):
    with open(LESSON_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

# Homepage
@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

# Public lesson route
@app.route('/lesson/<lesson_type>/<lang>')
def get_lesson(lesson_type, lang):
    lessons = load_lessons()
    lesson = lessons.get(lesson_type.lower())
    if lesson:
        content = lesson.get(lang.lower())
        if content:
            return jsonify({"content": content})
    return jsonify({"error": "Lesson not found"}), 404

# Video serving route
@app.route('/video/<filename>')
def get_video(filename):
    return send_from_directory('video', filename)

# Admin: Save or update lesson
@app.route('/admin/save', methods=['POST'])
def admin_save():
    data = request.json
    lesson_id = data.get("id")
    content = data.get("content")

    if not lesson_id or not content:
        return jsonify({"error": "Missing fields"}), 400

    lessons = load_lessons()
    lessons[lesson_id] = content
    save_lessons(lessons)

    return jsonify({"message": "Lesson saved successfully"})

# Admin: Delete a lesson
@app.route('/admin/delete/<lesson_id>', methods=['DELETE'])
def admin_delete(lesson_id):
    lessons = load_lessons()
    if lesson_id in lessons:
        del lessons[lesson_id]
        save_lessons(lessons)
        return jsonify({"message": "Lesson deleted"})
    else:
        return jsonify({"error": "Lesson not found"}), 404

# Run app
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
