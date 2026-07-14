import sqlite3
import getpass
from datetime import datetime


DATABASE = "users.db"


# -----------------------------
# Create database tables
# -----------------------------
def create_database():

    connection = sqlite3.connect(DATABASE)

    cursor = connection.cursor()


    # Users table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        created_at TEXT
    )
    """)


    # Sessions table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sessions(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        deaths INTEGER,
        pushups INTEGER,
        duration INTEGER,
        date TEXT,

        FOREIGN KEY(user_id)
        REFERENCES users(id)
    )
    """)


    connection.commit()
    connection.close()



# -----------------------------
# Get computer username
# -----------------------------
def get_username():

    return getpass.getuser()



# -----------------------------
# Find existing user
# or create new user
# -----------------------------
def get_or_create_user():

    username = get_username()


    connection = sqlite3.connect(DATABASE)

    cursor = connection.cursor()


    # Check if user exists
    cursor.execute(
        """
        SELECT id 
        FROM users
        WHERE username = ?
        """,
        (username,)
    )


    user = cursor.fetchone()



    if user:

        user_id = user[0]

        print(
            f"Welcome back {username}"
        )


    else:

        cursor.execute(
            """
            INSERT INTO users(
                username,
                created_at
            )
            VALUES (?,?)
            """,
            (
                username,
                datetime.now()
            )
        )


        user_id = cursor.lastrowid


        print(
            f"Created new user {username}"
        )



    connection.commit()
    connection.close()


    return user_id



# -----------------------------
# Save workout session
# -----------------------------
def save_session(
        user_id,
        deaths,
        pushups,
        duration
):

    connection = sqlite3.connect(DATABASE)

    cursor = connection.cursor()


    cursor.execute(
        """
        INSERT INTO sessions(
            user_id,
            deaths,
            pushups,
            duration,
            date
        )
        VALUES (?,?,?,?,?)
        """,
        (
            user_id,
            deaths,
            pushups,
            duration,
            datetime.now()
        )
    )


    connection.commit()
    connection.close()



# -----------------------------
# Get user statistics
# -----------------------------
def get_user_stats(user_id):

    connection = sqlite3.connect(DATABASE)

    cursor = connection.cursor()


    cursor.execute(
        """
        SELECT
            SUM(pushups),
            SUM(deaths),
            SUM(duration)
        FROM sessions
        WHERE user_id = ?
        """,
        (user_id,)
    )


    stats = cursor.fetchone()


    connection.close()


    return stats