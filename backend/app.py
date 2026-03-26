from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os, json
from utils import extract_text, clean_text, detect_skills, calculate_score, generate_suggestions

app = Flask(__name__, static_folder="../frontend", static_url_path="")
CORS(app)

with open(os.path.join(os.path.dirname(__file__), "skills.json"), "r") as f:
    SKILL_LIST = json.load(f)["skills"]

@app.route("/")
def home():
    return send_from_directory(app.static_folder, "index.html")

@app.route("/<path:path>")
def static_files(path):
    return send_from_directory(app.static_folder, path)

@app.route("/analyze", methods=["POST"])
def analyze_resume():
    try:
        if "file" not in request.files:
            return jsonify({"status": "error", "message": "No file uploaded"}), 400

        file = request.files["file"]
        filename = file.filename

        if not filename.lower().endswith((".pdf", ".txt")):
            return jsonify({"status": "error", "message": "Only PDF or TXT allowed"}), 400

        filepath = os.path.join("uploads", filename)
        os.makedirs("uploads", exist_ok=True)
        file.save(filepath)

        text = extract_text(filepath)
        if not text.strip():
            return jsonify({"status": "error", "message": "Empty or unreadable file"}), 400

        cleaned = clean_text(text)
        found_skills = detect_skills(cleaned, SKILL_LIST)
        score = calculate_score(found_skills, SKILL_LIST)
        suggestions = generate_suggestions(found_skills, SKILL_LIST)

        return jsonify({
            "status": "success",
            "score": score,
            "found_skills": found_skills,
            "missing_skills": list(set(SKILL_LIST) - set(found_skills)),
            "suggestions": suggestions
        })

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)