from flask import Flask, render_template, request, redirect, session
import sqlite3
from database import init_db

app = Flask(__name__)
app.secret_key = "SECRET123"   # Change this in production


# Helper: get database connection
def get_db():
    return sqlite3.connect("booking.db", check_same_thread=False)

@app.route("/")
def home():
    return render_template("home.html")

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
        username = request.form["username"]
        password = request.form["password"]
        db = get_db()
        c = db.cursor()
        c.execute("SELECT id FROM users WHERE username=? AND password=?", (username, password))
        user = c.fetchone()
        if user:
            session["user_id"] = user[0]
            session["username"] = username
            return redirect("/")
        else:
            return "Invalid login"
    return render_template("login.html")
def init_db():
    conn = sqlite3.connect("booking.db")
    c = conn.cursor()
    # Users table
    c.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
    """)

    # Ticket types table
    c.execute("""
    CREATE TABLE IF NOT EXISTS ticket_types(
        ticket_id INTEGER PRIMARY KEY AUTOINCREMENT,
        type TEXT NOT NULL,
        cost INTEGER NOT NULL
    )
    """)

    # Bookings table
    c.execute("""
    CREATE TABLE IF NOT EXISTS bookings(
        booking_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        ticket_id INTEGER NOT NULL,
        people INTEGER NOT NULL,
        date TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(id),
        FOREIGN KEY (ticket_id) REFERENCES ticket_types(ticket_id)
    )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS education (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        summary TEXT,
        image TEXT,
        content TEXT
    );
    """)
    c.execute("INSERT INTO ticket_types (type, cost) VALUES ('Adult', 30)")
    c.execute("INSERT INTO ticket_types (type, cost) VALUES ('Child', 20)")
    c.execute("INSERT INTO ticket_types (type, cost) VALUES ('Student', 20)")

    # Insert dummy educational articles ONCE
    existing = c.execute("SELECT COUNT(*) FROM education").fetchone()[0]

    if existing == 0:
        c.execute("""
            INSERT INTO education (title, summary, image, content)
            VALUES (?, ?, ?, ?)
        """, (
            "Amazing Tigers",
            "Find out fascinating facts about tigers, their habitats, and how they hunt.",
            "https://via.placeholder.com/600x350?text=Tigers",
            "Tigers are the largest cat species in the world. They live in Asia and are known for their strength, stealth, and striking orange-and-black striped fur..."
        ))

        c.execute("""
            INSERT INTO education (title, summary, image, content)
            VALUES (?, ?, ?, ?)
        """, (
            "Incredible Lions",
            "Learn why lions are known as the kings of the jungle.",
            "https://via.placeholder.com/600x350?text=Lions",
            "Lions are social animals that live in prides. They are powerful hunters and one of Africa’s most iconic species..."
        ))

        c.execute("""
            INSERT INTO education (title, summary, image, content)
            VALUES (?, ?, ?, ?)
        """, (
            "The World of Elephants",
            "Discover the largest land mammals on Earth.",
            "https://via.placeholder.com/600x350?text=Elephants",
            "Elephants are gentle giants known for their intelligence, memory, and complex family structures..."
        ))

        c.execute("""
            INSERT INTO education (title, summary, image, content)
            VALUES (?, ?, ?, ?)
        """, (
            "Giraffes and Their Long Necks",
            "Why do giraffes have long necks? Find out here!",
            "https://via.placeholder.com/600x350?text=Giraffes",
            "Giraffes use their long necks to browse tall trees and compete for food and mates..."
        ))

        c.execute("""
            INSERT INTO education (title, summary, image, content)
            VALUES (?, ?, ?, ?)
        """, (
            "Penguins of the Antarctic",
            "Explore how penguins survive freezing temperatures.",
            "https://via.placeholder.com/600x350?text=Penguins",
            "Penguins are flightless birds adapted for life in the water. Their thick layers of fat and feathers help them endure the icy Antarctic climate..."
        ))

    print("Inserted dummy educational articles!")

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

@app.route("/booking", methods=["GET", "POST"])
def booking():
    # must be logged in
    if "user_id" not in session:
        return redirect("/login")

    if request.method == "POST":
        selected_date = request.form["date"]
        adults = int(request.form["adults"])
        children = int(request.form["children"])
        students = int(request.form["students"])

        db = get_db()
        c = db.cursor()

        adultCost = c.execute("""
                        SELECT cost FROM ticket_types WHERE ticket_id = 1
                              """).fetchone()[0]
        totalAdultCost = 0

        childCost = c.execute("""
                        SELECT cost FROM ticket_types WHERE ticket_id = 2
                              """).fetchone()[0]
        totalChildCost = 0

        studentCost = c.execute("""
                        SELECT cost FROM ticket_types WHERE ticket_id = 3
                              """).fetchone()[0]
        totalStudentCost = 0
        # Insert each ticket type separately if > 0
        if adults > 0:
            totalAdultCost = adults * adultCost
            c.execute("""
                INSERT INTO bookings (user_id, ticket_id, people, date)
                VALUES (?, ?, ?, ?)
            """, (session["user_id"], 1, adults, selected_date))  # 1 = Adults

        if children > 0:
            totalChildCost = children * childCost

            c.execute("""
                INSERT INTO bookings (user_id, ticket_id, people, date)
                VALUES (?, ?, ?, ?)
            """, (session["user_id"], 2, children, selected_date))  # 2 = Children

        if students > 0:
            totalStudentCost = students * studentCost

            c.execute("""
                INSERT INTO bookings (user_id, ticket_id, people, date)
                VALUES (?, ?, ?, ?)
            """, (session["user_id"], 3, students, selected_date))  # 3 = Students

        db.commit()

        total_people = adults + children + students
        totalCost = totalStudentCost + totalChildCost + totalAdultCost
        return render_template("confirm.html", 
                               date=selected_date, 
                               people=total_people,
                               
                               adults=adults,
                               adultCost= adultCost,
                               totalAdultCost=totalAdultCost,

                               children=children,
                               childCost=childCost,
                               totalChildCost = totalChildCost,

                               students=students,
                               studentCost=studentCost,
                               totalStudentCost = totalStudentCost,

                               totalCost=totalCost)

    return render_template("booking.html")


@app.route("/education")
def education():
    db = get_db()
    #Return each row as a dictionary so can access by the name e.g. article['title']
    db.row_factory = sqlite3.Row  # <--- allows named access
    c = db.cursor()

    articles = c.execute("""
        SELECT * FROM education
    """).fetchall()

    return render_template("education.html", articles=articles)

@app.route("/article/<int:article_id>")
def article_detail(article_id):
    db = get_db()
    #Return each row as a dictionary so can access by the name e.g. article['title']
    db.row_factory = sqlite3.Row
    c = db.cursor()

    article = c.execute("""
        SELECT * FROM education WHERE id=?
    """, (article_id,)).fetchone()

    if article is None:
        return "Article not found", 404

    return render_template("article_detail.html", article=article)

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

if __name__ == "__main__":
    init_db()
    app.run(debug=True)