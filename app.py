from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)


# =========================================================
# DATABASE
# =========================================================

def get_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn


# =========================================================
# HOME / LOGIN
# =========================================================

@app.route("/")
def home():
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def login():

    username = request.form["username"]
    password = request.form["password"]
    role = request.form["role"]

    # Admin login
    if role == "admin" and username == "admin" and password == "admin123":
        return redirect("/admin_dashboard")

    # Student login
    elif role == "student" and username == "student" and password == "student123":
        return redirect("/student_dashboard")

    else:
        return """
        <h2>Invalid Username or Password</h2>
        <a href="/">Back to Login</a>
        """


# =========================================================
# ADMIN DASHBOARD
# =========================================================

@app.route("/admin_dashboard")
def admin_dashboard():

    conn = get_db()

    emergency_alerts = conn.execute(
        """
        SELECT * FROM emergency_alerts
        ORDER BY id DESC
        """
    ).fetchall()

    conn.close()

    return render_template(
        "admin_dashboard.html",
        emergency_alerts=emergency_alerts
    )


# =========================================================
# STUDENT DASHBOARD
# =========================================================

@app.route("/student_dashboard")
def student_dashboard():
    return render_template("student_dashboard.html")


# =========================================================
# STUDENTS
# =========================================================

@app.route("/students")
def students():

    conn = get_db()

    students = conn.execute(
        "SELECT * FROM students"
    ).fetchall()

    conn.close()

    return render_template(
        "students.html",
        students=students
    )


@app.route("/add_student", methods=["POST"])
def add_student():

    name = request.form["name"]
    email = request.form["email"]
    phone = request.form["phone"]
    room_no = request.form["room_no"]

    conn = get_db()

    conn.execute(
        """
        INSERT INTO students
        (name, email, phone, room_no)
        VALUES (?, ?, ?, ?)
        """,
        (name, email, phone, room_no)
    )

    conn.commit()
    conn.close()

    return redirect("/students")


# =========================================================
# ROOMS
# =========================================================

@app.route("/rooms")
def rooms():

    conn = get_db()

    rooms = conn.execute(
        "SELECT * FROM rooms"
    ).fetchall()

    conn.close()

    return render_template(
        "rooms.html",
        rooms=rooms
    )


@app.route("/add_room", methods=["POST"])
def add_room():

    room_no = request.form["room_no"]
    capacity = request.form["capacity"]

    conn = get_db()

    conn.execute(
        """
        INSERT INTO rooms
        (room_no, capacity, occupied, status)
        VALUES (?, ?, 0, 'Available')
        """,
        (room_no, capacity)
    )

    conn.commit()
    conn.close()

    return redirect("/rooms")


# =========================================================
# FEES
# =========================================================

@app.route("/fees")
def fees():

    conn = get_db()

    fees = conn.execute(
        "SELECT * FROM fees"
    ).fetchall()

    conn.close()

    return render_template(
        "fees.html",
        fees=fees
    )


@app.route("/add_fee", methods=["POST"])
def add_fee():

    student_name = request.form["student_name"]
    amount = request.form["amount"]
    payment_date = request.form["payment_date"]
    status = request.form["status"]

    conn = get_db()

    conn.execute(
        """
        INSERT INTO fees
        (student_name, amount, payment_date, status)
        VALUES (?, ?, ?, ?)
        """,
        (
            student_name,
            amount,
            payment_date,
            status
        )
    )

    conn.commit()
    conn.close()

    return redirect("/fees")


# =========================================================
# COMPLAINTS
# =========================================================

@app.route("/complaints")
def complaints():

    conn = get_db()

    complaints = conn.execute(
        "SELECT * FROM complaints"
    ).fetchall()

    conn.close()

    return render_template(
        "complaints.html",
        complaints=complaints
    )


@app.route("/add_complaint", methods=["POST"])
def add_complaint():

    student_name = request.form["student_name"]
    complaint = request.form["complaint"]
    date = request.form["date"]

    conn = get_db()

    conn.execute(
        """
        INSERT INTO complaints
        (student_name, complaint, status, date)
        VALUES (?, ?, 'Pending', ?)
        """,
        (
            student_name,
            complaint,
            date
        )
    )

    conn.commit()
    conn.close()

    return redirect("/complaints")


# =========================================================
# UPDATE COMPLAINT STATUS
# =========================================================

@app.route("/update_complaint/<int:id>", methods=["POST"])
def update_complaint(id):

    status = request.form["status"]

    conn = get_db()

    conn.execute(
        "UPDATE complaints SET status = ? WHERE id = ?",
        (status, id)
    )

    conn.commit()
    conn.close()

    return redirect("/complaints")


# =========================================================
# REPORTS
# =========================================================

@app.route("/reports")
def reports():

    conn = get_db()

    student_count = conn.execute(
        "SELECT COUNT(*) FROM students"
    ).fetchone()[0]

    room_count = conn.execute(
        "SELECT COUNT(*) FROM rooms"
    ).fetchone()[0]

    fee_count = conn.execute(
        "SELECT COUNT(*) FROM fees"
    ).fetchone()[0]

    complaint_count = conn.execute(
        "SELECT COUNT(*) FROM complaints"
    ).fetchone()[0]

    pending_complaints = conn.execute(
        "SELECT COUNT(*) FROM complaints WHERE status = 'Pending'"
    ).fetchone()[0]

    resolved_complaints = conn.execute(
        "SELECT COUNT(*) FROM complaints WHERE status = 'Resolved'"
    ).fetchone()[0]

    conn.close()

    return render_template(
        "reports.html",
        student_count=student_count,
        room_count=room_count,
        fee_count=fee_count,
        complaint_count=complaint_count,
        pending_complaints=pending_complaints,
        resolved_complaints=resolved_complaints
    )


# =========================================================
# ROOM ALLOCATION
# =========================================================

@app.route("/room_allocation")
def room_allocation():

    conn = get_db()

    allocations = conn.execute(
        "SELECT * FROM room_allocations"
    ).fetchall()

    conn.close()

    return render_template(
        "room_allocation.html",
        allocations=allocations
    )


@app.route("/allocate_room", methods=["POST"])
def allocate_room():

    student_name = request.form["student_name"]
    room_no = request.form["room_no"]
    allocation_date = request.form["allocation_date"]

    conn = get_db()

    # -----------------------------------------------------
    # Check whether room exists
    # -----------------------------------------------------

    room = conn.execute(
        "SELECT * FROM rooms WHERE room_no = ?",
        (room_no,)
    ).fetchone()

    if room is None:

        conn.close()

        return """
        <h2>Room Not Found!</h2>

        <p>Please add the room first.</p>

        <a href="/rooms">
            Back to Rooms
        </a>
        """


    # -----------------------------------------------------
    # Check whether room is already full
    # -----------------------------------------------------

    if room["occupied"] >= room["capacity"]:

        conn.close()

        return """
        <h2>Room is Full!</h2>

        <p>Please select another room.</p>

        <a href="/room_allocation">
            Back to Room Allocation
        </a>
        """


    # -----------------------------------------------------
    # Add room allocation
    # -----------------------------------------------------

    conn.execute(
        """
        INSERT INTO room_allocations
        (student_name, room_no, allocation_date)
        VALUES (?, ?, ?)
        """,
        (
            student_name,
            room_no,
            allocation_date
        )
    )


    # -----------------------------------------------------
    # Increase occupied count
    # -----------------------------------------------------

    new_occupied = room["occupied"] + 1


    # -----------------------------------------------------
    # Update room status
    # -----------------------------------------------------

    if new_occupied >= room["capacity"]:
        status = "Full"
    else:
        status = "Available"


    conn.execute(
        """
        UPDATE rooms
        SET occupied = ?, status = ?
        WHERE room_no = ?
        """,
        (
            new_occupied,
            status,
            room_no
        )
    )


    # -----------------------------------------------------
    # Save changes
    # -----------------------------------------------------

    conn.commit()
    conn.close()

    return redirect("/room_allocation")

# =========================================================
# CHECK-IN / CHECK-OUT
# =========================================================

@app.route("/checkin_checkout", methods=["GET", "POST"])
def checkin_checkout():

    conn = get_db()

    if request.method == "POST":

        student_name = request.form["student_name"]
        room_no = request.form["room_no"]
        date = request.form["date"]
        action = request.form["action"]

        conn.execute(
            """
            INSERT INTO checkin_checkout
            (student_name, room_no, date, action)
            VALUES (?, ?, ?, ?)
            """,
            (
                student_name,
                room_no,
                date,
                action
            )
        )

        conn.commit()

    records = conn.execute(
        """
        SELECT * FROM checkin_checkout
        ORDER BY id DESC
        """
    ).fetchall()

    conn.close()

    return render_template(
        "checkin_checkout.html",
        records=records
    )
# =========================================================
# ATTENDANCE
# =========================================================

@app.route("/attendance", methods=["GET", "POST"])
def attendance():

    conn = get_db()

    if request.method == "POST":

        student_name = request.form["student_name"]
        room_no = request.form["room_no"]
        date = request.form["date"]
        status = request.form["status"]

        conn.execute(
            """
            INSERT INTO attendance
            (student_name, room_no, date, status)
            VALUES (?, ?, ?, ?)
            """,
            (
                student_name,
                room_no,
                date,
                status
            )
        )

        conn.commit()

    records = conn.execute(
        """
        SELECT * FROM attendance
        ORDER BY id DESC
        """
    ).fetchall()

    conn.close()

    return render_template(
        "attendance.html",
        records=records
    )
# =========================================================
# SOS / EMERGENCY HELP
# =========================================================

# =========================================================
# SOS / EMERGENCY HELP
# =========================================================

@app.route("/sos", methods=["GET", "POST"])
def sos():

    conn = get_db()

    if request.method == "POST":

        student_name = request.form["student_name"]
        message = request.form["message"]

        conn.execute(
            """
            INSERT INTO emergency_alerts
            (student_name, message, date, status)
            VALUES (?, ?, datetime('now'), 'Emergency')
            """,
            (student_name, message)
        )

        conn.commit()
        conn.close()

        return """
        <h2>🚨 Emergency Alert Sent!</h2>
        <p>The Admin / Warden has been notified.</p>
        <a href="/sos">Back to SOS</a>
        """

    conn.close()

    return render_template("sos.html")
# =========================================================
# RUN APPLICATION
# =========================================================

if __name__ == "__main__":
    print("Hostel & PG Management System")
    print("Admin Dashboard: http://127.0.0.1:5001/admin_dashboard")
    print("Student Dashboard: http://127.0.0.1:5001/student_dashboard")
    print("SOS Emergency Help: http://127.0.0.1:5001/sos")

    import os

app.run(
    host="0.0.0.0",
    port=int(os.environ.get("PORT", 5001)),
    debug=True
)