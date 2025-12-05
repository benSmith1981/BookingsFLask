from app import get_db

def init_db():
    conn = get_db()
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
            "https://tse4.mm.bing.net/th/id/OIP.cdqbyBTd4Ud1-q5dQI13hgHaE8?pid=Apis",
            "Tigers are the largest cat species in the world. They live in Asia and are known for their strength, stealth, and striking orange-and-black striped fur..."
        ))

        c.execute("""
            INSERT INTO education (title, summary, image, content)
            VALUES (?, ?, ?, ?)
        """, (
            "Incredible Lions",
            "Learn why lions are known as the kings of the jungle.",
            "https://cdn.mos.cms.futurecdn.net/FVqUjfbiHS9imyJiRiM53-970-80.jpg",
            "Lions are social animals that live in prides. They are powerful hunters and one of Africa’s most iconic species..."
        ))

        c.execute("""
            INSERT INTO education (title, summary, image, content)
            VALUES (?, ?, ?, ?)
        """, (
            "The World of Elephants",
            "Discover the largest land mammals on Earth.",
            "https://tse2.mm.bing.net/th/id/OIP.ELuQSsbszrUeguQbDScoKAHaJ4?pid=Api",
            "Elephants are gentle giants known for their intelligence, memory, and complex family structures..."
        ))

        c.execute("""
            INSERT INTO education (title, summary, image, content)
            VALUES (?, ?, ?, ?)
        """, (
            "Giraffes and Their Long Necks",
            "Why do giraffes have long necks? Find out here!",
            "https://tse2.mm.bing.net/th/id/OIP.6dLjDPlPCzhPjG8kK96qZQHaKT?pid=Api",
            "Giraffes use their long necks to browse tall trees and compete for food and mates..."
        ))

        c.execute("""
            INSERT INTO education (title, summary, image, content)
            VALUES (?, ?, ?, ?)
        """, (
            "Penguins of the Antarctic",
            "Explore how penguins survive freezing temperatures.",
            "https://tse3.mm.bing.net/th/id/OIP.t1p8TBohAPgQjzfvfwAsLgHaFj?pid=Api",
            "Penguins are flightless birds adapted for life in the water. Their thick layers of fat and feathers help them endure the icy Antarctic climate..."
        ))

    print("Inserted dummy educational articles!")

    conn.commit()
    conn.close()