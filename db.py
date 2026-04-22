"""Database connection helper for School Transport Route DB."""

import mysql.connector
from mysql.connector import Error


DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "root",  # Change this to your MySQL password
    "database": "school_transport_db",
}


def get_connection():
    """Create and return a MySQL database connection."""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except Error as exc:
        print(f"Database connection failed: {exc}")
        return None
