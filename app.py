from flask import Flask, render_template
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

@app.route("/users")
def users():
    data = get_users()
    return render_template("users.html", users=data)

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)
