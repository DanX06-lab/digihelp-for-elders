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

# Auto-generate HTML lesson page
def generate_html_page(lesson_id):
    template = f"""<!DOCTYPE html>
<html lang=\"en\">
<head>
  <meta charset=\"UTF-8\" />
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\" />
  <title>{lesson_id.title()} Lesson – DigiHelp</title>
  <link href=\"https://fonts.googleapis.com/css2?family=Poppins:wght@300;600&display=swap\" rel=\"stylesheet\" />
  <style>
    body {{ font-family: 'Poppins', sans-serif; background-color: #121212; color: #f5f5f5; padding: 2rem; }}
    h1 {{ text-align: center; }}
    #lesson-content {{ background: #1e1e1e; padding: 1.5rem; border-radius: 10px; margin-top: 1rem; white-space: pre-line; }}
    video {{ display: block; margin: 1rem auto; max-width: 800px; width: 100%; border-radius: 12px; }}
    select {{ background: #222; color: #fff; padding: 10px; border: 1px solid #333; border-radius: 5px; display: block; margin: 1rem auto; }}
    a {{ color: #66b2ff; display: block; text-align: center; margin-top: 2rem; text-decoration: none; }}
  </style>
</head>
<body>
  <h1>{lesson_id.title()} Lesson</h1>
  <div style=\"text-align:center;\">
    <label for=\"language\">🌐 Language:</label>
    <select id=\"language\" onchange=\"loadLesson()\">
      <option value=\"en\">English</option>
      <option value=\"hi\">हिन्दी</option>
      <option value=\"bn\">বাংলা</option>
    </select>
  </div>
  <div id=\"lesson-content\">Loading lesson...</div>
  <video id=\"lesson-video\" controls style=\"display:none;\">
    <source id=\"video-source\" src=\"\" type=\"video/mp4\">
  </video>
  <a href=\"../index.html\">⬅ Back to Home</a>
  <script>
    const lessonId = \"{lesson_id}\";
    function loadLesson() {{
      const lang = document.getElementById("language").value;
      fetch(`https://digihelp-for-elders.onrender.com/lesson/${{lessonId}}/${{lang}}`)
        .then(res => res.json())
        .then(data => {{
          document.getElementById("lesson-content").innerText = data.content || "No content found.";
          const video = document.getElementById("lesson-video");
          const source = document.getElementById("video-source");
          source.src = `../videos/${{lessonId}}_${{lang}}.mp4`;
          video.style.display = "block";
          video.load();
        }})
        .catch(() => {{
          document.getElementById("lesson-content").innerText = "Failed to load content.";
        }});
    }}
    window.onload = loadLesson;
  </script>
</body>
</html>"""
    os.makedirs("lessons", exist_ok=True)
    with open(f"lessons/{lesson_id}.html", "w", encoding="utf-8") as f:
        f.write(template)

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

# List all lesson IDs (used for dynamic homepage)
@app.route('/lessons')
def get_all_lessons():
    lessons = load_lessons()
    return jsonify({"lessons": list(lessons.keys())})

# Admin: Save or update lesson
@app.route('/admin/save', methods=['POST'])
def admin_save():
    data = request.json
    lesson_id = data.get("id", "").strip().lower()
    content = data.get("content", {})

    if not lesson_id or not isinstance(content, dict):
        return jsonify({"error": "Missing or invalid fields"}), 400

    lessons = load_lessons()
    is_new = lesson_id not in lessons

    lessons[lesson_id] = content
    save_lessons(lessons)

    if is_new:
        generate_html_page(lesson_id)

    message = "New lesson added!" if is_new else "Lesson updated successfully"
    return jsonify({"message": message})

# Admin: Delete a lesson
@app.route('/admin/delete/<lesson_id>', methods=['DELETE'])
def admin_delete(lesson_id):
    lesson_id = lesson_id.strip().lower()
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
