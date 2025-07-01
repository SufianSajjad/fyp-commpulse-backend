# db/setup.py

import psycopg2
import os

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

DB_NAME = os.getenv('DB_NAME', 'commpulse_db')
DB_USER = os.getenv('DB_USER', 'commpulse_user')
DB_PASS = os.getenv('DB_PASS', 'commpulse_password')
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '5432')
SUPERUSER_PASS = os.getenv('SUPERUSER_PASS', 'postgres')

def create_database_and_user():
    """
    Connect to PostgreSQL as superuser (e.g., 'postgres'), 
    create the database (if it doesn't exist), and create a normal user.
    """
    try:
        # Connect to the default 'postgres' database with superuser
        conn = psycopg2.connect(
            dbname='postgres',
            user='postgres',            # superuser name
            password=SUPERUSER_PASS,    # superuser password
            host=DB_HOST,
            port=DB_PORT
        )
        conn.autocommit = True
        cursor = conn.cursor()

        # Create the database
        cursor.execute(f"CREATE DATABASE {DB_NAME} OWNER postgres;")

        # Create a dedicated user for your app
        cursor.execute(f"CREATE USER {DB_USER} WITH PASSWORD '{DB_PASS}';")

        # Grant privileges
        cursor.execute(f"GRANT ALL PRIVILEGES ON DATABASE {DB_NAME} TO {DB_USER};")

        cursor.close()
        conn.close()
        print("✅ Database and user created successfully!")
    except Exception as e:
        print("Error creating database/user:", e)

if __name__ == '__main__':
    create_database_and_user()
