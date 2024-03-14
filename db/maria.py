# src/db/maria.py

import mysql.connector
from mysql.connector import Error
import os

DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_USER = os.getenv('DB_USER', 'root')
DB_PASS = os.getenv('DB_PASS', '1234')
DB_NAME = os.getenv('DB_NAME', 'chat_bot')

def create_connection():
    """Create a database connection to a MariaDB server."""
    connection = None
    try:
        connection = mysql.connector.connect(
            host = DB_HOST,
            user = DB_USER,
            passwd = DB_PASS,
            database = DB_NAME
        )
        print("MariaDB connection successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection
