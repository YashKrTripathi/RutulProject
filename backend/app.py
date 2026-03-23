from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime
import re

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///thumbnails.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Board(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

class Thumbnail(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    board_id = db.Column(db.Integer, db.ForeignKey('board.id'), nullable=False)

    url = db.Column(db.String(500))
    imageUrl = db.Column(db.String(500))
    title = db.Column(db.String(200))
    channel = db.Column(db.String(100))
    category = db.Column(db.String(50))
    score = db.Column(db.Integer)
    views = db.Column(db.String(50))
    saved = db.Column(db.Boolean, default=False)
    notes = db.Column(db.Text)
    addedAt = db.Column(db.DateTime, default=datetime.utcnow)

def extract_video_id(url):
    match = re.search(r"(?:v=|youtu\.be/)([^&\n?#]+)", url)
    return match.group(1) if match else None

def get_thumbnail(url):
    video_id = extract_video_id(url)
    if video_id:
        return f"http://img.youtube.com/vi/{video_id}/0.jpg"
    return None

@app.route("/boards", methods=["POST"])
def create_board():
    data = request.json
    board = Board(name=data.get("name"))
    db.session.add(board)
    db.session.commit()
    return jsonify({"id": board.id, "name": board.name})

@app.route("/boards", methods=["GET"])
def get_boards():
    boards = Board.query.all()
    return jsonify([{"id": b.id, "name": b.name} for b in boards])

@app.route("/boards/<int:board_id>/thumbnails", methods=["POST"])
def add_thumbnail(board_id):
    data = request.json
    url = data.get("url")
    image_url = get_thumbnail(url)

    if not image_url:
        return jsonify({"error": "Invalid YouTube URL"}), 400

    thumb = Thumbnail(
        board_id=board_id,
        url=url,
        imageUrl=image_url,
        title=data.get("title", "Untitled"),
        channel=data.get("channel", "Unknown"),
        category=data.get("category", "Other"),
        score=data.get("score", 50),
        views=data.get("views", "—"),
        saved=False,
        notes=""
    )

    db.session.add(thumb)
    db.session.commit()
    return jsonify({"id": thumb.id})

@app.route("/boards/<int:board_id>/thumbnails", methods=["GET"])
def get_thumbnails(board_id):
    thumbs = Thumbnail.query.filter_by(board_id=board_id).all()
    return jsonify([{
        "id": t.id,
        "url": t.url,
        "imageUrl": t.imageUrl,
        "title": t.title,
        "channel": t.channel,
        "category": t.category,
        "score": t.score,
        "views": t.views,
        "saved": t.saved,
        "notes": t.notes,
        "addedAt": t.addedAt.isoformat()
    } for t in thumbs])

@app.route("/thumbnails/<int:id>", methods=["PUT"])
def update_thumbnail(id):
    t = Thumbnail.query.get(id)
    data = request.json
    t.title = data.get("title", t.title)
    t.score = data.get("score", t.score)
    t.notes = data.get("notes", t.notes)
    t.saved = data.get("saved", t.saved)
    db.session.commit()
    return jsonify({"message": "Updated"})

@app.route("/thumbnails/<int:id>", methods=["DELETE"])
def delete_thumbnail(id):
    t = Thumbnail.query.get(id)
    db.session.delete(t)
    db.session.commit()
    return jsonify({"message": "Deleted"})

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
