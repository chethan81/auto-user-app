from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)

DB_PATH = "users.db"

# Create database automatically
def init_db():
    if not os.path.exists(DB_PATH):
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL
            );
        """)
        cur.executemany(
            "INSERT INTO users (name, email) VALUES (?, ?)",
            [
                ("Chethan", "chethan@example.com"),
                ("Ravi", "ravi@example.com"),
                ("Kiran", "kiran@example.com")
            ]
        )
        conn.commit()
        conn.close()

def get_users():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM users")
    rows = cur.fetchall()
    conn.close()
    return rows

@app.route("/")
def home():
    return "Auto User App Running Successfully!"

def insert_user(name, email):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("INSERT INTO users (name, email) VALUES (?, ?)", (name, email))
    conn.commit()
    conn.close()

def get_user_by_id(user_id):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = cur.fetchone()
    conn.close()
    return user

@app.route("/users", methods=["GET", "POST"])
def users():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        if name and email:
            insert_user(name, email)
        return redirect(url_for("users"))
    
    data = get_users()
    return render_template("users.html", users=data)

@app.route("/user/<int:user_id>")
def user_detail(user_id):
    user = get_user_by_id(user_id)
    if user is None:
        return "User not found", 404
    return render_template("user_detail.html", user=user)

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)
