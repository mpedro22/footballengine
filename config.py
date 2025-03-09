import os
from dotenv import load_dotenv
import mysql.connector

# Load variabel dari .env
load_dotenv()

# Database Config
DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASS"),
    "database": os.getenv("DB_NAME"),
}

# API Config
API_URL = "http://api.football-data.org/v4"
API_KEY = os.getenv("API_KEY")

# Fungsi untuk koneksi ke database
def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)
