from dotenv import load_dotenv
import os

load_dotenv()

DB_CONFIG = {
    "host": os.getenv("POSTGRES_HOST"),
    "port": os.getenv("POSTGRES_PORT"),
    "user": os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRES_PASSWORD"),
    "dbname": os.getenv("POSTGRES_DB")
}

FILE_EXTENSION = [".jpg", ".jpeg", ".png", ".gif"]

MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

HOST = "0.0.0.0"
PORT = 8000
