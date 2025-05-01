# db/mysql_connection.py

import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", "1234@Bcd"),
        database=os.getenv("DB_NAME", "etchlin_db"),
        port=os.getenv("DB_PORT", 3306)
    )
