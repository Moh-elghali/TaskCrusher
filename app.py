from flask import Flask, redirect, render_template, request, session, flash
from flask_session import Session
from cs50 import SQL
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from datetime import date

app = Flask(__name__)

# Use filesystem sessions, same as CS50 Finance pset
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Connect to SQLite database via CS50 library
db = SQL("sqlite:///tasks.db")


def login_required(f):
    """Redirect to login if user is not signed in."""
    @wraps(f)
    def decorated(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated


# ── Routes ────────────────────────────────────────────────────────────────────

@app.route("/")
@login_required
def index():
    """Homepage — show all of the user's tasks."""
    tasks = db.execute(
        "SELECT * FROM tasks WHERE user_id = ? ORDER BY done ASC, created DESC",
        session["user_id"]
    )
    name = db.execute("SELECT username FROM users WHERE id = ?", session["user_id"])[0]["username"]
    today = date.today().isoformat()
    hour  = date.today().timetuple().tm_hour  # can't use datetime in template easily
    from datetime import datetime
    hour = datetime.now().hour
    return render_template("index.html", tasks=tasks, name=name, today=today, hour=hour)


@app.route("/add", methods=["POST"])
@login_required
def add():
    """Add a new task."""
    title = request.form.get("title", "").strip()
    note  = request.form.get("note", "").strip()
    due   = request.form.get("due", "")

    if not title:
        flash("Give your task a title first!")
        return redirect("/")

    db.execute(
        "INSERT INTO tasks (user_id, title, note, due) VALUES (?, ?, ?, ?)",
        session["user_id"], title, note, due or None
    )
    flash("Task added! Now go crush it 💪")
    return redirect("/")


@app.route("/done/<int:task_id>", methods=["POST"])
@login_required
def done(task_id):
    """Toggle a task between done and not done."""
    db.execute(
        "UPDATE tasks SET done = NOT done WHERE id = ? AND user_id = ?",
        task_id, session["user_id"]
    )
    return redirect("/")


@app.route("/delete/<int:task_id>", methods=["POST"])
@login_required
def delete(task_id):
    """Delete a task permanently."""
    db.execute(
        "DELETE FROM tasks WHERE id = ? AND user_id = ?",
        task_id, session["user_id"]
    )
    flash("Task deleted.")
    return redirect("/")


@app.route("/edit/<int:task_id>", methods=["GET", "POST"])
@login_required
def edit(task_id):
    """Edit an existing task."""
    task = db.execute(
        "SELECT * FROM tasks WHERE id = ? AND user_id = ?",
        task_id, session["user_id"]
    )
    if not task:
        flash("Task not found.")
        return redirect("/")
    task = task[0]

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        note  = request.form.get("note", "").strip()
        due   = request.form.get("due", "")

        if not title:
            flash("Title can't be empty.")
            return render_template("edit.html", task=task)

        db.execute(
            "UPDATE tasks SET title = ?, note = ?, due = ? WHERE id = ? AND user_id = ?",
            title, note, due or None, task_id, session["user_id"]
        )
        flash("Task updated ✅")
        return redirect("/")

    return render_template("edit.html", task=task)


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register a new user."""
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        confirm  = request.form.get("confirm", "")

        if not username:
            flash("Please pick a username.")
            return render_template("register.html")
        if not password:
            flash("Please enter a password.")
            return render_template("register.html")
        if password != confirm:
            flash("Passwords don't match — try again.")
            return render_template("register.html")
        if len(password) < 6:
            flash("Password needs at least 6 characters.")
            return render_template("register.html")

        existing = db.execute("SELECT id FROM users WHERE username = ?", username)
        if existing:
            flash("That username is taken, pick another.")
            return render_template("register.html")

        user_id = db.execute(
            "INSERT INTO users (username, hash) VALUES (?, ?)",
            username, generate_password_hash(password)
        )
        session["user_id"] = user_id
        flash(f"Welcome, {username}! Your account is ready 🎉")
        return redirect("/")

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log in an existing user."""
    session.clear()

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        rows = db.execute("SELECT * FROM users WHERE username = ?", username)
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], password):
            flash("Wrong username or password.")
            return render_template("login.html")

        session["user_id"] = rows[0]["id"]
        flash(f"Hey {username}, good to see you 👋")
        return redirect("/")

    return render_template("login.html")


@app.route("/logout")
def logout():
    """Log the user out."""
    session.clear()
    return redirect("/login")
