def load_config():
    """Returns the database connection configuration."""
    return {
        "dbname": "phonebook_db", # Make sure to create this database in pgAdmin or psql first
        "user": "postgres",       # Your PostgreSQL username
        "password": "password",   # Your PostgreSQL password
        "host": "localhost",
        "port": "5432"
    }