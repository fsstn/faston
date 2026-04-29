import psycopg2
from config import DB_CONFIG


def get_connection():
    """just connect to the database using the settings from config"""
    return psycopg2.connect(**DB_CONFIG)