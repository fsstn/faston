import psycopg2
from config import load_config

def connect():
    """Connect to the PostgreSQL database server."""
    try:
        params = load_config()
        print("Connecting to the PostgreSQL database...")
        conn = psycopg2.connect(**params)
        return conn
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Connection error: {error}")
        return None