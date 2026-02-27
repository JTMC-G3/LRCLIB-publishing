#!/usr/bin/env python3
"""
lyrics_syncer Flask app

Setup:
    pip install flask

Run:
    python app.py

Then open http://localhost:5000 in your browser.
"""

import json
import os
from pathlib import Path
from flask import Flask, render_template, request, jsonify, send_file

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "uploads1"
os.makedirs("uploads1", exist_ok=True)


@app.route("/")
def index():
    return render_template("lyricssync.html")


@app.route("/upload", methods=["POST"])
def upload():
    mp3 = request.files.get("mp3")
    lyrics = request.files.get("lyrics")

    if not mp3 or not lyrics:
        return jsonify({"error": "Both an MP3 and a lyrics file are required."}), 400

    mp3_path = Path(app.config["UPLOAD_FOLDER"]) / "song.mp3"
    lyrics_path = Path(app.config["UPLOAD_FOLDER"]) / "lyrics.txt"

    mp3.save(mp3_path)
    lyrics.save(lyrics_path)

    lines = [
        l.strip()
        for l in lyrics_path.read_text(encoding="utf-8").splitlines()
        if l.strip()
    ]

    song_name = Path(mp3.filename).stem

    return jsonify({"lines": lines, "song_name": song_name})


@app.route("/audio")
def audio():
    path = Path(app.config["UPLOAD_FOLDER"]) / "song.mp3"
    if not path.exists():
        return "No audio uploaded", 404
    return send_file(path, mimetype="audio/mpeg")


@app.route("/export", methods=["POST"])
def export():
    data = request.get_json()
    output = {
        "type": "synced",
        "lines": data.get("lines", []),
        "matched_title": data.get("matched_title", ""),
    }
    out_path = Path(app.config["UPLOAD_FOLDER"]) / "synced.json"
    out_path.write_text(json.dumps(output, indent=2, ensure_ascii=False))
    return send_file(out_path, as_attachment=True, download_name="synced.json", mimetype="application/json")


if __name__ == "__main__":
    app.run(debug=True, port=5000)