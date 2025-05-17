import sqlite3

def initialize_db():
    connection = sqlite3.connect("appointments.db")
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS appointments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            time DATETIME NOT NULL UNIQUE
        )
    """)
    connection.commit()
    connection.close()


# Database file
DB_FILE = 'appointments.db'


def connect_db():
    """Establish a connection to the SQLite database."""
    return sqlite3.connect(DB_FILE)


def fetch_appointments():
    """Fetch all appointments from the database."""
    conn = connect_db()
    cursor = conn.cursor()

    # Query to fetch all appointments
    query = "SELECT name, time FROM appointments ORDER BY time ASC"
    cursor.execute(query)

    appointments = cursor.fetchall()

    conn.close()

    return appointments


def check_appointment_time(appointment_time):
    """Check if the appointment time already exists in the database (unique within 1 minute)."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Query to check if the time already exists
    query = "SELECT 1 FROM appointments WHERE time = ?"
    cursor.execute(query, (appointment_time,))

    # If a row is returned, the time is already taken
    result = cursor.fetchone()

    conn.close()

    # Return True if the time is taken, otherwise False
    return result is not None


def add_appointment(name, appointment_time):
    """Add a new appointment to the database."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Insert the new appointment into the appointments table
    query = "INSERT INTO appointments (name, time) VALUES (?, ?)"
    cursor.execute(query, (name, appointment_time))

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

def delete_appointment(name):
    """Delete an appointment by name."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Query to delete the appointment by name
    query = "DELETE FROM appointments WHERE name = ?"
    cursor.execute(query, (name,))
    conn.commit()
    conn.close()

def update_appointment_time(name, new_time):
    """Update the appointment time for a given name."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Query to update the time
    query = "UPDATE appointments SET time = ? WHERE name = ?"
    cursor.execute(query, (new_time, name))
    conn.commit()
    conn.close()


