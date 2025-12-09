import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    return mysql.connector.connect(
        host=os.environ.get("DB_HOST", "db"),
        user=os.environ.get("DB_USER", "app"),
        password=os.environ.get("DB_PASSWORD", "apppass"),
        database=os.environ.get("DB_NAME", "phone_service"),
        autocommit=True
    )

def execute(query, params=None, fetch=False):
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, params or ())
        if fetch:
            return cursor.fetchall()
        return cursor
    finally:
        if conn:
            conn.close()
