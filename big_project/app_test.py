# Frames - Photo sharing web application
# author: Stephen Kerr

import os # for file handling and path operations
import sqlite3 # for database interactions
# Flask framework and utilities 
#   (jsonify for JSON responses, request for handling incoming data, 
#    g for global context), send_from_directory for serving static files, 
#   session for user sessions, redirect and url_for for navigation
from flask import Flask, jsonify, request, g, send_from_directory, session, redirect, url_for 
from werkzeug.utils import secure_filename # for safely handling uploaded file names
from werkzeug.security import generate_password_hash, check_password_hash # for password hashing 
from functools import wraps # for creating decorators (e.g., for authentication)
import secrets # for generating secure tokens



app = Flask(__name__)
app.secret_key = "change-this-to-something-random-in-production"


# --- Config ---
DATABASE    = "frames.db"
UPLOAD_FOLDER = "static/uploads"
ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "gif", "webp"}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# --- DB helpers ---
def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db

@app.teardown_appcontext
def close_db(error):
    db = g.pop("db", None)
    if db is not None:
        db.close()

def init_db():
    db = get_db()
    db.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id            INTEGER   PRIMARY KEY AUTOINCREMENT,
            email         TEXT      NOT NULL UNIQUE,
            password_hash TEXT      NOT NULL,
            role          TEXT      NOT NULL DEFAULT 'organiser',
            created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    db.execute("""
        CREATE TABLE IF NOT EXISTS albums (
            id               INTEGER   PRIMARY KEY AUTOINCREMENT,
            name             TEXT      NOT NULL,
            description      TEXT,
            event_date       TEXT,
            slug             TEXT      NOT NULL UNIQUE,
            created_by_admin INTEGER   REFERENCES users(id),
            organiser_id     INTEGER   REFERENCES users(id),
            created_at       TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    db.execute("""
        CREATE TABLE IF NOT EXISTS photos (
            id          INTEGER   PRIMARY KEY AUTOINCREMENT,
            album_id    INTEGER   NOT NULL REFERENCES albums(id) ON DELETE CASCADE,
            filename    TEXT      NOT NULL,
            filepath    TEXT      NOT NULL,
            uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    db.execute("""
        CREATE TABLE IF NOT EXISTS qr_redirects (
            id         INTEGER   PRIMARY KEY AUTOINCREMENT,
            album_id   INTEGER   NOT NULL UNIQUE REFERENCES albums(id) ON DELETE CASCADE,
            token      TEXT      NOT NULL UNIQUE,
            target_url TEXT      NOT NULL,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_by INTEGER   REFERENCES users(id)
        )
    """)
    db.commit()

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


# Protects any route that requires a login
def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated


# ---------------------------------------------------------------
# ALBUM ROUTES
# ---------------------------------------------------------------

# login
# GET serves the login page, POST processes the login form
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")

        user = get_db().execute(
            "SELECT * FROM users WHERE email = ?", (email,)
        ).fetchone()

        if user is None or not check_password_hash(user["password_hash"], password):
            return jsonify({"error": "Invalid credentials"}), 401

        # Write to the session — this is what "being logged in" means
        session["user_id"] = user["id"]
        session["role"] = user["role"]
        return jsonify({"role": user["role"]}), 200

    return send_from_directory("static", "login.html")


# logout
@app.route("/logout", methods=["POST"])
def logout():
    session.clear()  # Wipes the session — user is now logged out
    return jsonify({"message": "Logged out"}), 200


# admin user seed
def seed_admin():
    db = get_db()
    existing = db.execute("SELECT id FROM users WHERE role = 'admin'").fetchone()
    if existing:
        print("Admin already exists, skipping seed")
        return
    db.execute(
        "INSERT INTO users (email, password_hash, role) VALUES (?, ?, ?)",
        ("admin@frames.com", generate_password_hash("changeme123"), "admin")
    )
    db.commit()
    print("Admin seeded: admin@frames.com / changeme123")

# admin
@app.route("/admin")
@login_required
def admin_page():
    if session["role"] != "admin":
        return jsonify({"error": "Forbidden"}), 403
    return send_from_directory("static", "admin.html")


# POST create organiser account — admin only
@app.route("/users", methods=["POST"])
@login_required
def create_organiser():
    if session["role"] != "admin":
        return jsonify({"error": "Forbidden"}), 403
    data = request.get_json()
    if not data or "email" not in data or "password" not in data:
        return jsonify({"error": "email and password are required"}), 400
    db = get_db()
    # Check if email already exists
    if db.execute("SELECT id FROM users WHERE email = ?", (data["email"],)).fetchone():
        return jsonify({"error": "Email already in use"}), 409
    db.execute(
        "INSERT INTO users (email, password_hash, role) VALUES (?, ?, ?)",
        (data["email"], generate_password_hash(data["password"]), "organiser")
    )
    db.commit()
    return jsonify({"message": "Organiser created"}), 201


# Guest upload page — no login required
@app.route("/upload/<slug>")
def upload_page(slug):
    album = get_db().execute(
        "SELECT * FROM albums WHERE slug = ?", (slug,)
    ).fetchone()
    if album is None:
        return "Album not found", 404
    return send_from_directory("static", "upload.html")


# GET all organisers — admin only
@app.route("/users", methods=["GET"])
@login_required
def get_organisers():
    if session["role"] != "admin":
        return jsonify({"error": "Forbidden"}), 403
    rows = get_db().execute(
        "SELECT id, email FROM users WHERE role = 'organiser'"
    ).fetchall()
    return jsonify([dict(r) for r in rows]), 200


# PATCH assign organiser to album — admin only
@app.route("/albums/<int:album_id>/assign", methods=["PATCH"])
@login_required
def assign_organiser(album_id):
    if session["role"] != "admin":
        return jsonify({"error": "Forbidden"}), 403
    data = request.get_json()
    if "organiser_id" not in data:
        return jsonify({"error": "organiser_id is required"}), 400
    db = get_db()
    if db.execute("SELECT id FROM albums WHERE id = ?", (album_id,)).fetchone() is None:
        return jsonify({"error": "Album not found"}), 404
    db.execute(
        "UPDATE albums SET organiser_id = ? WHERE id = ?",
        (data["organiser_id"], album_id)
    )
    db.commit()
    return jsonify({"message": "Organiser assigned"}), 200




# Serve the organiser dashboard page
@app.route("/dashboard")
@login_required
def dashboard_page():
    if session["role"] != "organiser":
        return jsonify({"error": "Forbidden"}), 403
    return send_from_directory("static", "dashboard.html")


# GET the album assigned to the logged-in organiser
@app.route("/my-album", methods=["GET"])
@login_required
def my_album():
    album = get_db().execute(
        "SELECT * FROM albums WHERE organiser_id = ?", (session["user_id"],)
    ).fetchone()
    if album is None:
        return jsonify({"error": "No album assigned"}), 404
    return jsonify(dict(album)), 200


# Guest photo upload — no login required
@app.route("/upload/<slug>/photo", methods=["POST"])
def guest_upload_photo(slug):
    album = get_db().execute(
        "SELECT * FROM albums WHERE slug = ?", (slug,)
    ).fetchone()
    if album is None:
        return jsonify({"error": "Album not found"}), 404
    if "photo" not in request.files:
        return jsonify({"error": "No file provided"}), 400
    file = request.files["photo"]
    if file.filename == "" or not allowed_file(file.filename):
        return jsonify({"error": "Invalid file type"}), 400

    filename = secure_filename(file.filename)
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    db = get_db()
    cursor = db.execute(
        "INSERT INTO photos (filename, filepath, album_id) VALUES (?, ?, ?)",
        (filename, filepath, album["id"])
    )
    db.commit()
    row = db.execute("SELECT * FROM photos WHERE id = ?", (cursor.lastrowid,)).fetchone()
    return jsonify(dict(row)), 201


# GET all albums
@app.route("/albums", methods=["GET"])
def get_albums():
    rows = get_db().execute("SELECT * FROM albums ORDER BY created_at DESC").fetchall()
    return jsonify([dict(r) for r in rows]), 200

# GET one album
@app.route("/albums/<int:album_id>", methods=["GET"])
def get_album(album_id):
    row = get_db().execute("SELECT * FROM albums WHERE id = ?", (album_id,)).fetchone()
    if row is None:
        return jsonify({"error": "Album not found"}), 404
    return jsonify(dict(row)), 200

# POST create album
@app.route("/albums", methods=["POST"])
@login_required
def create_album():
    if session["role"] != "admin":
        return jsonify({"error": "Forbidden"}), 403
    data = request.get_json()
    if not data or "name" not in data or "slug" not in data:
        return jsonify({"error": "name and slug are required"}), 400
    db = get_db()
    cursor = db.execute(
        "INSERT INTO albums (name, description, event_date, slug, created_by_admin) VALUES (?, ?, ?, ?, ?)",
        (data["name"], data.get("description"), data.get("event_date"), data["slug"], session["user_id"])
    )
    db.commit()
    row = db.execute("SELECT * FROM albums WHERE id = ?", (cursor.lastrowid,)).fetchone()
    return jsonify(dict(row)), 201

# PATCH update album
@app.route("/albums/<int:album_id>", methods=["PATCH"])
def update_album(album_id):
    db = get_db()
    row = db.execute("SELECT * FROM albums WHERE id = ?", (album_id,)).fetchone()
    if row is None:
        return jsonify({"error": "Album not found"}), 404
    data = request.get_json()
    name = data.get("name", row["name"])
    db.execute("UPDATE albums SET name = ? WHERE id = ?", (name, album_id))
    db.commit()
    updated = db.execute("SELECT * FROM albums WHERE id = ?", (album_id,)).fetchone()
    return jsonify(dict(updated)), 200

# DELETE album (cascades to photos)
@app.route("/albums/<int:album_id>", methods=["DELETE"])
def delete_album(album_id):
    db = get_db()
    if db.execute("SELECT id FROM albums WHERE id = ?", (album_id,)).fetchone() is None:
        return jsonify({"error": "Album not found"}), 404
    db.execute("DELETE FROM albums WHERE id = ?", (album_id,))
    db.commit()
    return "", 204


# ---------------------------------------------------------------
# PHOTO ROUTES
# ---------------------------------------------------------------

# GET all photos in an album
@app.route("/albums/<int:album_id>/photos", methods=["GET"])
def get_photos(album_id):
    if get_db().execute("SELECT id FROM albums WHERE id = ?", (album_id,)).fetchone() is None:
        return jsonify({"error": "Album not found"}), 404
    rows = get_db().execute(
        "SELECT * FROM photos WHERE album_id = ? ORDER BY uploaded_at DESC", (album_id,)
    ).fetchall()
    return jsonify([dict(r) for r in rows]), 200

# GET one photo
@app.route("/photos/<int:photo_id>", methods=["GET"])
def get_photo(photo_id):
    row = get_db().execute("SELECT * FROM photos WHERE id = ?", (photo_id,)).fetchone()
    if row is None:
        return jsonify({"error": "Photo not found"}), 404
    return jsonify(dict(row)), 200

# POST upload a photo to an album
@app.route("/albums/<int:album_id>/photos", methods=["POST"])
def upload_photo(album_id):
    if get_db().execute("SELECT id FROM albums WHERE id = ?", (album_id,)).fetchone() is None:
        return jsonify({"error": "Album not found"}), 404
    if "photo" not in request.files:
        return jsonify({"error": "No file provided"}), 400
    file = request.files["photo"]
    if file.filename == "" or not allowed_file(file.filename):
        return jsonify({"error": "Invalid file type"}), 400
    filename = secure_filename(file.filename)
    file.save(os.path.join(UPLOAD_FOLDER, filename))
    db = get_db()
    cursor = db.execute(
        "INSERT INTO photos (filename, album_id) VALUES (?, ?)", (filename, album_id)
    )
    db.commit()
    row = db.execute("SELECT * FROM photos WHERE id = ?", (cursor.lastrowid,)).fetchone()
    return jsonify(dict(row)), 201

# DELETE a photo
@app.route("/photos/<int:photo_id>", methods=["DELETE"])
def delete_photo(photo_id):
    db = get_db()
    row = db.execute("SELECT * FROM photos WHERE id = ?", (photo_id,)).fetchone()
    if row is None:
        return jsonify({"error": "Photo not found"}), 404
    filepath = os.path.join(UPLOAD_FOLDER, row["filename"])
    if os.path.exists(filepath):
        os.remove(filepath)
    db.execute("DELETE FROM photos WHERE id = ?", (photo_id,))
    db.commit()
    return "", 204


# Serve the frontend from the static folder
@app.route("/")
def index():
    return send_from_directory("static", "index.html")


@app.route("/album")
def album_page():
    return send_from_directory("static", "album.html")


if __name__ == "__main__":
    with app.app_context():
        init_db()
        seed_admin()
    app.run(debug=True)
