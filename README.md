# Placement Portal Application - V2

A full-stack web application for managing campus placements. Students, companies, and the institute admin interact through role-based dashboards.

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Flask, Flask-RESTful, Flask-Security-Too |
| Frontend | Vue 3, Pinia, Vue Router, Bootstrap 5 |
| Database | SQLite + SQLAlchemy ORM |
| Cache | Redis + Flask-Caching |
| Jobs | Celery + Celery Beat |
| Email | Mailhog (local SMTP) |

---

## Project Structure

```
project/
├── backend/
│   ├── main.py
│   ├── models.py
│   ├── config.py
│   ├── database.py
│   ├── user_datastore.py
│   ├── cache.py
│   ├── mail.py
│   ├── celery_app.py
│   ├── tasks.py
│   ├── static/
│   │   ├── resumes/
│   │   └── exports/
│   └── controllers/
│       ├── auth.py
│       ├── student.py
│       ├── company.py
│       └── admin.py
└── frontend/
    └── src/
        ├── App.vue
        ├── main.js
        ├── router/index.js
        ├── stores/
        │   ├── auth.js
        │   └── message.js
        └── views/
            ├── Home.vue
            ├── Login.vue
            ├── Register.vue
            ├── admin/
            ├── company/
            └── student/
```

---

## Setup & Run

### Prerequisites

- Python 3.10+
- Node.js 18+
- Redis server
- Mailhog

---

### 1. Backend

```bash
cd backend

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate        # Linux/Mac
venv\Scripts\activate           # Windows

# Install dependencies
pip install flask flask-restful flask-security-too flask-sqlalchemy \
            flask-cors flask-caching celery redis werkzeug bcrypt

# Run Flask server
python main.py
```

Backend runs at `http://127.0.0.1:5000`

Admin is seeded automatically:
- Email: `admin@ppa.com`
- Password: `admin`

---

### 2. Frontend

```bash
cd frontend

# Install dependencies
npm install

# Run dev server
npm run dev
```

Frontend runs at `http://localhost:5173`

---

### 3. Redis

```bash
# Linux
redis-server

# Mac
brew services start redis
```

Redis runs at `localhost:6379`

---

### 4. Mailhog (Email Testing)

```bash
# Linux
./MailHog_linux_amd64

# Mac
brew install mailhog && mailhog
```

- SMTP port: `1025` (used internally by the app)
- Web UI: `http://localhost:8025` (view emails here)

---

### 5. Celery Worker (Background Jobs)

```bash
cd backend
source venv/bin/activate

celery -A tasks worker --loglevel=info
```

---

### 6. Celery Beat (Scheduled Jobs)

```bash
cd backend
source venv/bin/activate

celery -A tasks beat --loglevel=info
```

---

## Running All Services (Summary)

Open 5 terminals from the `backend/` folder:

| Terminal | Command |
|----------|---------|
| 1 | `python main.py` |
| 2 | `redis-server` |
| 3 | `celery -A tasks worker --loglevel=info` |
| 4 | `celery -A tasks beat --loglevel=info` |
| 5 | `mailhog` |

And one terminal from `frontend/`:

| Terminal | Command |
|----------|---------|
| 6 | `npm run dev` |

---

## Key Features

- Role-based access: Admin, Company, Student
- Token-based authentication via Flask-Security
- Company and drive approval workflow
- Server-side eligibility validation on apply
- Resume upload (PDF, stored on disk)
- CSV export of application history (async, email alert on done)
- Daily deadline reminders to eligible students (Celery Beat)
- Monthly HTML activity report to admin (Celery Beat)
- Redis caching on high-traffic endpoints with cache invalidation
- Global flash messages via Pinia message store

---

## Notes

- Delete `backend/instance/ppa.db` and restart if you need a fresh database.
- For demo purposes, change Celery Beat schedule in `celery_app.py` from `crontab` to `60.0` (seconds) to trigger jobs every minute.
- All emails are caught locally by Mailhog — no real emails are sent.
