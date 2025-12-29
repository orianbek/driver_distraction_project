import sqlite3
from datetime import datetime
DB_NAME = "ddd.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    # Users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL
        )
    """)

    # Events table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            event_type TEXT NOT NULL,
            username TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


def add_user(username, password, role):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
            (username, password, role)
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()


def check_login(username, password):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT role FROM users WHERE username=? AND password=?",
        (username, password)
    )
    result = cursor.fetchone()
    conn.close()

    if result:
        return result[0]   # role
    return None

def insert_event(username, event_type):
    conn = get_connection()
    cursor = conn.cursor()

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute(
        "INSERT INTO events (timestamp, event_type, username) VALUES (?, ?, ?)",
        (timestamp, event_type, username)
    )

    conn.commit()
    conn.close()

def get_all_events():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT timestamp, username, event_type FROM events ORDER BY timestamp DESC"
    )
    events = cursor.fetchall()
    conn.close()

    return events


##if __name__ == "__main__":
##    create_tables()
##    add_user("orian", "1234", "admin")
##    add_user("avital", "4321", "driver")
##    print("DB initialized")


