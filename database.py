import sqlite3
def init_db():
    conn = sqlite3.connect("booking.db")
    c = conn.cursor()
    # Create users table
    c.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)
    # Create bookings table
    c.execute("""
        CREATE TABLE IF NOT EXISTS bookings(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
<<<<<<< Updated upstream
            user_id INTEGER,
            date TEXT,
=======
            user_id INTEGER NOT NULL,
            people INTEGER,
            date TEXT NOT NULL,
>>>>>>> Stashed changes
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)
    conn.commit()
    conn.close()
if __name__ == "__main__":
    init_db()