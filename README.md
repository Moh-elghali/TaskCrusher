# Taskly — CS50x Final Project

**A simple, friendly task manager built with Flask, SQLite, and plain HTML/CSS/JS.**

---

## What it does

Taskly lets you keep track of things you need to do. You can:

- **Register** a personal account and **log in** securely
- **Add tasks** with an optional note and due date
- **Check off** tasks when you're done (and uncheck them if you change your mind)
- **Edit** a task if the details change
- **Delete** tasks you no longer need
- See a friendly **greeting** and a count of what's still pending
- Tasks that are **overdue** are highlighted in red so nothing slips through

---

## How to run it

### 1. Open the folder in VS Code

### 2. Create a virtual environment
```bash
python -m venv venv
```

### 3. Activate it
```bash
# Windows
venv\Scripts\activate

# Mac / Linux
source venv/bin/activate
```

### 4. Install dependencies
```bash
pip install -r requirements.txt
```

### 5. Create the database
```bash
sqlite3 tasks.db < schema.sql
```

### 6. Run the app
```bash
flask run
```

Then open **http://127.0.0.1:5000** in your browser.

---

## Project structure

```
taskly/
├── app.py              ← All Flask routes
├── schema.sql          ← SQL to create the database tables
├── tasks.db            ← SQLite database (created after step 5)
├── requirements.txt
├── README.md
├── templates/
│   ├── layout.html     ← Shared page shell (nav, flash messages)
│   ├── login.html
│   ├── register.html
│   ├── index.html      ← Main dashboard
│   └── edit.html
└── static/
    ├── css/style.css
    └── js/app.js
```

---

## CS50x topics used

| Topic | Where |
|---|---|
| Python | `app.py` — routes, logic, decorators |
| Flask  | Web framework — routes, sessions, Jinja2 |
| SQL    | `schema.sql` + `db.execute()` in `app.py` |
| HTML   | All 5 templates |
| CSS    | `static/css/style.css` |
| JavaScript | `static/js/app.js` (flash dismiss, date inputs) |
| Hashing | `werkzeug` — passwords stored as hashes, never plaintext |
| Sessions | `flask-session` — keeps users logged in |

---

Made for CS50x 🎓
