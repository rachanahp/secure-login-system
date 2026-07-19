"""
Secure Login System
--------------------
A simple Flask web application demonstrating secure authentication practices:
- Password hashing with bcrypt
- Protection from SQL injection using parameterized queries
- Session management with login/logout
- Optional simple 2FA (One-Time Passcode simulation)
"""

import sqlite3
import random
from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "replace-this-with-a-random-secret-key"  # change before deploying

DB_NAME = "users.db"


def init_db():
    """Creates the users table if it doesn't already exist."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/")
def home():
    if "username" in session:
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        if not username or not password:
            flash("Username and password are required.")
            return redirect(url_for("register"))

        if len(password) < 6:
            flash("Password must be at least 6 characters long.")
            return redirect(url_for("register"))

        # Hash the password securely (scrypt via Werkzeug)
        password_hash = generate_password_hash(password)

        conn = get_db_connection()
        try:
            # Parameterized query - protects against SQL injection
            conn.execute(
                "INSERT INTO users (username, password_hash) VALUES (?, ?)",
                (username, password_hash)
            )
            conn.commit()
            flash("Registration successful! Please log in.")
            return redirect(url_for("login"))
        except sqlite3.IntegrityError:
            flash("That username is already taken.")
            return redirect(url_for("register"))
        finally:
            conn.close()

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        conn = get_db_connection()
        # Parameterized query - protects against SQL injection
        user = conn.execute(
            "SELECT * FROM users WHERE username = ?", (username,)
        ).fetchone()
        conn.close()

        if user and check_password_hash(user["password_hash"], password):
            # Generate a simple OTP for demonstration of 2FA
            otp = str(random.randint(100000, 999999))
            session["pending_user"] = username
            session["otp"] = otp
            # In a real app, you would email or SMS this OTP to the user.
            # For this demo, we display it directly (for testing purposes only).
            flash(f"Your OTP (for demo purposes) is: {otp}")
            return redirect(url_for("verify_otp"))
        else:
            flash("Invalid username or password.")
            return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/verify-otp", methods=["GET", "POST"])
def verify_otp():
    if "pending_user" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        entered_otp = request.form.get("otp", "").strip()
        if entered_otp == session.get("otp"):
            session["username"] = session.pop("pending_user")
            session.pop("otp", None)
            flash("Login successful!")
            return redirect(url_for("dashboard"))
        else:
            flash("Incorrect OTP. Please try again.")
            return redirect(url_for("verify_otp"))

    return render_template("verify_otp.html")


@app.route("/dashboard")
def dashboard():
    if "username" not in session:
        return redirect(url_for("login"))
    return render_template("dashboard.html", username=session["username"])


@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.")
    return redirect(url_for("login"))


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
