import sqlite3

conn = sqlite3.connect("database.db")

conn.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT,
    phone TEXT,
    room_no TEXT
)
""")

conn.execute("""
CREATE TABLE IF NOT EXISTS rooms (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    room_no TEXT NOT NULL,
    capacity INTEGER,
    occupied INTEGER DEFAULT 0,
    status TEXT DEFAULT 'Available'
)
""")

conn.execute("""
CREATE TABLE IF NOT EXISTS fees (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_name TEXT NOT NULL,
    amount REAL NOT NULL,
    payment_date TEXT,
    status TEXT DEFAULT 'Pending'
)
""")

conn.execute("""
CREATE TABLE IF NOT EXISTS complaints (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_name TEXT NOT NULL,
    complaint TEXT NOT NULL,
    status TEXT DEFAULT 'Pending',
    date TEXT
)
""")
conn.execute("""
CREATE TABLE IF NOT EXISTS room_allocations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_name TEXT NOT NULL,
    room_no TEXT NOT NULL,
    allocation_date TEXT
)
""")
conn.execute("""
CREATE TABLE IF NOT EXISTS checkin_checkout (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_name TEXT NOT NULL,
    room_no TEXT NOT NULL,
    date TEXT,
    action TEXT NOT NULL
)
""")
conn.execute("""
CREATE TABLE IF NOT EXISTS attendance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_name TEXT NOT NULL,
    room_no TEXT NOT NULL,
    date TEXT NOT NULL,
    status TEXT NOT NULL
)
""")
conn.execute("""
CREATE TABLE IF NOT EXISTS emergency_alerts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_name TEXT NOT NULL,
    message TEXT NOT NULL,
    date TEXT NOT NULL,
    status TEXT NOT NULL
)
""")
conn.commit()
conn.close()

print("Database setup completed successfully!")