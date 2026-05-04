# Web Services and Applications -> Big Project: Frames
by Stephen Kerr

## Purpose of this Repository
This repository contains the big project submission for the module ***Web Services and Applications*** taught by Andrew Beatty as part of the HDIP in Computing and Data Analytics. To learn more about the HDIP review the link here: [HDIP in Computing and Data Analytics](https://www.atu.ie/courses/higher-diploma-in-science-data-analytics)

**Frames** is a Flask-based event photo sharing web application. The idea is simple an event organiser prints a QR code, guests scan it on their phones and upload photos directly to the event album, and the organiser can view, download and manage everything from their dashboard. No app download required for guests.

 
> **Live hosted version:** [https://stephenk17.pythonanywhere.com](https://stephenk17.pythonanywhere.com)

Logins per user role to test the hosted web app: 
- Admin: 
    - Email: admin@frames.com
    - Password: changeme123

- Organiser: 
    - Email: andrew@lecturer.com
    - Password: bestapp100

- Guest:
    - No login required but need to have an upload link / QR code.

---

## Technologies Used
- Python 3.13
- Flask & Werkzeug
- SQLite (via Python sqlite3)
- segno (QR code generation)
- HTML, CSS & JavaScript
- Git & GitHub
- Visual Studio Code
- PythonAnywhere (hosting)

---

## How to Run Locally

**1. Clone the repository**
```bash
git clone https://github.com/skerr17/web_services_-_applications.git
cd web_services_-_applications/big_project
```

**2. Create and activate a virtual environment**
```bash
python -m venv venv
venv\Scripts\activate      # Windows
source venv/bin/activate   # Mac/Linux
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Create a `config.py` file in the project root**
```python
keys = {
    "SECRET_KEY": "your-secret-key-here"
}

admin_credentials = {
    "username": "admin@frames.com",
    "password": "your-admin-password"
}
```

**5. Run the app**
```bash
python main_app.py
```

The app will be available at `http://127.0.0.1:5000`. The database and uploads folder are created automatically on first run. The admin account is seeded from `config.py` on startup.

---

## Project Structure

```
big_project/
├── main_app.py            # Flask application — all routes and logic
├── qr_code_generator.py   # QR code generation module using segno
├── config.py              # Secret key and admin credentials (not committed)
├── frames.db              # SQLite database (auto-created on first run)
├── requirements.txt       # Python dependencies
├── static/
│   ├── css/
│   │   └── frames.css     # Shared stylesheet across all pages
│   ├── images/
│   │   └── logo.svg
│   ├── uploads/           # Uploaded photos (auto-created on first run)
│   ├── admin.html
│   ├── album.html
│   ├── dashboard.html
│   ├── login.html
│   └── upload.html
└── README.md
```

---

## Application Overview

Frames has three user roles each with their own view and permissions:

### Admin
The admin is the platform owner. They can create and delete albums and organiser accounts, assign organisers to albums, view all albums and photos, and manage QR redirects. The key feature here is the ability to update what a printed QR code points to without reprinting (useful if the wrong album was linked after QR codes were already distributed at an event).

### Organiser
The organiser is typically the photographer or event coordinator. After logging in they see their assigned album, can copy the guest upload link or download the QR code for printing, upload photos themselves, and view, download or delete all photos in the album.

### Guest
No login required. Guests scan the QR code or follow a link, and upload one or more photos directly from their phone. The upload page is deliberately minimal and mobile-optimised.

---

## API Routes Summary

| Method | Route | Auth | Description |
|--------|-------|------|-------------|
| GET/POST | `/` | None | Login page and login handler |
| POST | `/logout` | Login | Clear session |
| GET | `/admin` | Admin | Admin panel |
| GET | `/dashboard` | Login | Organiser dashboard |
| GET | `/album` | Admin | Album view (`?id=`) |
| GET | `/upload/<slug>` | None | Guest upload page |
| GET/POST | `/users` | Admin | List / create organisers |
| DELETE | `/users/<id>` | Admin | Delete organiser |
| GET/POST | `/albums` | None/Admin | List all / create album |
| GET/PATCH/DELETE | `/albums/<id>` | None/Admin | Get / update / delete album |
| PATCH | `/albums/<id>/assign` | Admin | Assign organiser to album |
| GET | `/my-album` | Login | Get current organiser's album |
| GET/POST | `/albums/<id>/photos` | None | List / upload photos |
| POST | `/upload/<slug>/photo` | None | Guest photo upload |
| DELETE | `/photos/<id>` | None | Delete photo |
| GET | `/r/<token>` | None | Public QR redirect |
| GET/PATCH | `/qr/<id>` | Login/Admin | Get / update QR redirect |
| GET | `/albums/<id>/qr` | Login | Get QR code as PNG |

---

## Key Design Decisions

- **Dynamic QR redirects** — each album gets a permanent token (e.g. `/r/xk92pL`) that redirects to a configurable target. Printed QR codes never need reprinting even if the target changes.
- **Filename collision prevention** — uploaded photos are prefixed with a random 6-byte hex string to prevent files with the same name overwriting each other.
- **`PRAGMA foreign_keys = ON`** — set per connection since SQLite disables FK enforcement by default. This ensures cascade deletes work correctly.

---

## Future Development

- Per-event welcome message and theming on the guest upload page and album
- Logo overlay on QR codes for event branding
- Bulk photo download as a ZIP file
- Email notification to organiser when new photos are uploaded
- Profile Management page with user creation path 
- Photo slideshow capability for an album for an interactive way of sharing photos with guests


---
 
## References and AI Usage
 
### External Libraries
- [Flask](https://flask.palletsprojects.com/) — web framework
- [Werkzeug](https://werkzeug.palletsprojects.com/) — password hashing and secure filename handling
- [segno](https://segno.readthedocs.io/) — QR code generation

### AI Usage
Claude (Anthropic) was used during development as a coding assistant — primarily for debugging, reviewing code structure, and generating boilerplate. All code was written, reviewed and understood by me (Stephen Kerr). Prompts used included things like: *"review this Flask route for security issues"*, and *"check this README for anything missing from the project brief"*.
 

---

## End