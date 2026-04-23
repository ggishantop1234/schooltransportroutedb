"""Flask app for School Transport Route DB mini project."""

from flask import Flask, render_template, request, redirect, url_for, flash
from db import get_connection

app = Flask(__name__)
app.secret_key = "dev-secret-key"


@app.route("/")
def index():
    """Dashboard page with quick stats."""
    connection = get_connection()
    stats = {
        "students": 0,
        "buses": 0,
        "routes": 0,
        "drivers": 0,
    }
    if connection:
        cursor = connection.cursor(dictionary=True)
        for key, table in [
            ("students", "students"),
            ("buses", "buses"),
            ("routes", "routes"),
            ("drivers", "drivers"),
        ]:
            cursor.execute(f"SELECT COUNT(*) AS total FROM {table}")
            stats[key] = cursor.fetchone()["total"]
        cursor.close()
        connection.close()
    return render_template("index.html", stats=stats)


@app.route("/buses", methods=["GET", "POST"])
def buses():
    """Create and list buses."""
    connection = get_connection()
    if not connection:
        flash("Could not connect to database.", "danger")
        return render_template("buses.html", buses=[])

    cursor = connection.cursor(dictionary=True)

    if request.method == "POST":
        bus_number = request.form["bus_number"]
        capacity = request.form["capacity"]
        cursor.execute(
            "INSERT INTO buses (bus_number, capacity) VALUES (%s, %s)",
            (bus_number, capacity),
        )
        connection.commit()
        flash("Bus added successfully.", "success")
        return redirect(url_for("buses"))

    cursor.execute("SELECT * FROM buses ORDER BY bus_id DESC")
    bus_rows = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template("buses.html", buses=bus_rows)


@app.route("/drivers", methods=["GET", "POST"])
def drivers():
    """Create and list drivers."""
    connection = get_connection()
    if not connection:
        flash("Could not connect to database.", "danger")
        return render_template("drivers.html", drivers=[])

    cursor = connection.cursor(dictionary=True)

    if request.method == "POST":
        name = request.form["name"]
        phone = request.form["phone"]
        license_no = request.form["license_no"]
        cursor.execute(
            "INSERT INTO drivers (name, phone, license_no) VALUES (%s, %s, %s)",
            (name, phone, license_no),
        )
        connection.commit()
        flash("Driver added successfully.", "success")
        return redirect(url_for("drivers"))

    cursor.execute("SELECT * FROM drivers ORDER BY driver_id DESC")
    driver_rows = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template("drivers.html", drivers=driver_rows)


@app.route("/routes", methods=["GET", "POST"])
def routes():
    """Create and list routes with bus and driver assignment."""
    connection = get_connection()
    if not connection:
        flash("Could not connect to database.", "danger")
        return render_template("routes.html", routes=[], buses=[], drivers=[])

    cursor = connection.cursor(dictionary=True)

    if request.method == "POST":
        route_name = request.form["route_name"]
        start_point = request.form["start_point"]
        end_point = request.form["end_point"]
        bus_id = request.form["bus_id"]
        driver_id = request.form["driver_id"]
        cursor.execute(
            """
            INSERT INTO routes (route_name, start_point, end_point, bus_id, driver_id)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (route_name, start_point, end_point, bus_id, driver_id),
        )
        connection.commit()
        flash("Route created successfully.", "success")
        return redirect(url_for("routes"))

    cursor.execute("SELECT * FROM buses")
    bus_rows = cursor.fetchall()
    cursor.execute("SELECT * FROM drivers")
    driver_rows = cursor.fetchall()

    cursor.execute(
        """
        SELECT r.route_id, r.route_name, r.start_point, r.end_point,
               b.bus_number, d.name AS driver_name
        FROM routes r
        JOIN buses b ON r.bus_id = b.bus_id
        JOIN drivers d ON r.driver_id = d.driver_id
        ORDER BY r.route_id DESC
        """
    )
    route_rows = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template(
        "routes.html",
        routes=route_rows,
        buses=bus_rows,
        drivers=driver_rows,
    )


@app.route("/stops", methods=["GET", "POST"])
def stops():
    """Create and list bus stops per route."""
    connection = get_connection()
    if not connection:
        flash("Could not connect to database.", "danger")
        return render_template("stops.html", stops=[], routes=[])

    cursor = connection.cursor(dictionary=True)

    if request.method == "POST":
        stop_name = request.form["stop_name"]
        area = request.form["area"]
        route_id = request.form["route_id"]
        cursor.execute(
            "INSERT INTO stops (stop_name, area, route_id) VALUES (%s, %s, %s)",
            (stop_name, area, route_id),
        )
        connection.commit()
        flash("Stop added successfully.", "success")
        return redirect(url_for("stops"))

    cursor.execute("SELECT route_id, route_name FROM routes")
    route_rows = cursor.fetchall()

    cursor.execute(
        """
        SELECT s.stop_id, s.stop_name, s.area, r.route_name
        FROM stops s
        JOIN routes r ON s.route_id = r.route_id
        ORDER BY s.stop_id DESC
        """
    )
    stop_rows = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template("stops.html", stops=stop_rows, routes=route_rows)


@app.route("/students", methods=["GET", "POST"])
def students():
    """Create and list students with assigned stop and route."""
    connection = get_connection()
    if not connection:
        flash("Could not connect to database.", "danger")
        return render_template("students.html", students=[], stops=[])

    cursor = connection.cursor(dictionary=True)

    if request.method == "POST":
        student_name = request.form["student_name"]
        grade = request.form["grade"]
        phone = request.form["phone"]
        stop_id = request.form["stop_id"]
        cursor.execute(
            """
            INSERT INTO students (student_name, grade, phone, stop_id)
            VALUES (%s, %s, %s, %s)
            """,
            (student_name, grade, phone, stop_id),
        )
        connection.commit()
        flash("Student added successfully.", "success")
        return redirect(url_for("students"))

    cursor.execute(
        """
        SELECT s.stop_id, s.stop_name, r.route_name
        FROM stops s
        JOIN routes r ON s.route_id = r.route_id
        ORDER BY s.stop_name
        """
    )
    stop_rows = cursor.fetchall()

    cursor.execute(
        """
        SELECT st.student_id, st.student_name, st.grade, st.phone,
               sp.stop_name, r.route_name, b.bus_number
        FROM students st
        JOIN stops sp ON st.stop_id = sp.stop_id
        JOIN routes r ON sp.route_id = r.route_id
        JOIN buses b ON r.bus_id = b.bus_id
        ORDER BY st.student_id DESC
        """
    )
    student_rows = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template("students.html", students=student_rows, stops=stop_rows)


@app.route("/reports")
def reports():
    """Show simple analytical reports using SQL joins and grouping."""
    connection = get_connection()
    if not connection:
        flash("Could not connect to database.", "danger")
        return render_template("reports.html", student_report=[], route_counts=[])

    cursor = connection.cursor(dictionary=True)
    cursor.execute(
        """
        SELECT st.student_name, st.grade, sp.stop_name, r.route_name,
               b.bus_number, d.name AS driver_name
        FROM students st
        JOIN stops sp ON st.stop_id = sp.stop_id
        JOIN routes r ON sp.route_id = r.route_id
        JOIN buses b ON r.bus_id = b.bus_id
        JOIN drivers d ON r.driver_id = d.driver_id
        ORDER BY st.student_name
        """
    )
    student_report = cursor.fetchall()

    cursor.execute(
        """
        SELECT r.route_name, COUNT(st.student_id) AS student_count
        FROM routes r
        LEFT JOIN stops sp ON r.route_id = sp.route_id
        LEFT JOIN students st ON sp.stop_id = st.stop_id
        GROUP BY r.route_id, r.route_name
        ORDER BY r.route_name
        """
    )
    route_counts = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template(
        "reports.html",
        student_report=student_report,
        route_counts=route_counts,
    )


@app.route("/delete/<string:table>/<int:record_id>", methods=["POST"])
def delete_record(table, record_id):
    """Simple delete endpoint for demo purposes."""
    allowed = {
        "buses": "bus_id",
        "drivers": "driver_id",
        "routes": "route_id",
        "stops": "stop_id",
        "students": "student_id",
    }

    if table not in allowed:
        flash("Invalid delete request.", "danger")
        return redirect(url_for("index"))

    connection = get_connection()
    if connection:
        cursor = connection.cursor()
        cursor.execute(
            f"DELETE FROM {table} WHERE {allowed[table]} = %s",
            (record_id,),
        )
        connection.commit()
        cursor.close()
        connection.close()
        flash(f"Deleted record from {table}.", "warning")

    return redirect(url_for(table))


if __name__ == "__main__":
    app.run(debug=True)
