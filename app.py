from flask import Flask, render_template, request, redirect, session, jsonify
import sqlite3
from database import init_db
import firebase_admin
from firebase_admin import credentials, auth
app = Flask(__name__)
app.secret_key = "SECRET123"   # Change this in production

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
# Helper: get database connection
def get_db():
    return sqlite3.connect("booking.db", check_same_thread=False)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        db = get_db()
        c = db.cursor()
        # Insert new user
        try:
            c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            db.commit()
        except:
            return "User already exists"
        return redirect("/login")
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        id_token = request.headers.get("Authorization")

        if not id_token:
            return jsonify({"error": "Missing Authorization header"}), 401

        if id_token.startswith("Bearer "):
            id_token = id_token.split("Bearer ")[1]

        try:
            decoded_token = auth.verify_id_token(id_token)
            uid = decoded_token["uid"]
            email = decoded_token.get("email")

            session["user_id"] = uid
            session["email"] = email

            return jsonify({"message": f"Welcome {email}"})
        except Exception as e:
            return jsonify({"error": str(e)}), 401

    return render_template("login.html")

def init_db():
    conn = sqlite3.connect("booking.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS bookings(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            date TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)
    conn.commit()
    conn.close()

@app.route("/my-bookings")
def my_bookings():
    if "user_id" not in session:
        return redirect("/login")
    db = get_db()
    c = db.cursor()
    c.execute("SELECT date FROM bookings WHERE user_id=?", (session["user_id"],))
    rows = c.fetchall()
    return render_template("bookings.html", bookings=rows)

@app.route("/", methods=["GET", "POST"])
def booking():
    if "user_id" not in session:
        return redirect("/login")

    if request.method == "POST":
        selected_date = request.form["date"]
        db = get_db()
        c = db.cursor()
        c.execute("INSERT INTO bookings (user_id, date) VALUES (?, ?)", (session["user_id"], selected_date))
        db.commit()
        return render_template("confirm.html", date=selected_date)

    return render_template("booking.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

if __name__ == "__main__":
    init_db()
    app.run(debug=True)