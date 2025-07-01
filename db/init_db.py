# db/init_db.py

import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

DB_NAME = os.getenv('DB_NAME', 'commpulse_db')
DB_USER = os.getenv('DB_USER', 'commpulse_user')
DB_PASS = os.getenv('DB_PASS', 'commpulse_password')
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '5432')

def init_tables():
    """
    Connects to the database as the normal user and creates tables:
      - user
      - meeting
      - meeting_participants
      - transcripts (optional, for storing meeting transcript data)
    """
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASS,
            host=DB_HOST,
            port=DB_PORT
        )
        cursor = conn.cursor()

        # 1) User Table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS "user" (
            user_id SERIAL PRIMARY KEY,
            username VARCHAR(100) UNIQUE NOT NULL,
            email VARCHAR(255) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL,
            full_name VARCHAR(255),
            created_at TIMESTAMP DEFAULT NOW()
        );
        """)

        # 2) Meeting Table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS "meeting" (
            meeting_id SERIAL PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            agenda TEXT,
            start_time TIMESTAMP,
            end_time TIMESTAMP,
            created_at TIMESTAMP DEFAULT NOW()
        );
        """)

        # 3) Meeting Participants (speaker stats per meeting)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS meeting_participants (
            participant_id SERIAL PRIMARY KEY,
            user_id INT NOT NULL REFERENCES "user"(user_id) ON DELETE CASCADE,
            meeting_id INT NOT NULL REFERENCES "meeting"(meeting_id) ON DELETE CASCADE,
            active_participation NUMERIC(5,2),
            sentiment NUMERIC(5,2),
            agenda_adherence NUMERIC(5,2),
            clarity NUMERIC(5,2),
            joined_at TIMESTAMP DEFAULT NOW()
        );
        """)

        # 4) Transcripts Table (optional, for summary generation)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS transcripts (
            transcript_id SERIAL PRIMARY KEY,
            meeting_id INT NOT NULL REFERENCES "meeting"(meeting_id) ON DELETE CASCADE,
            content TEXT,
            created_at TIMESTAMP DEFAULT NOW()
        );
        """)

        conn.commit()
        cursor.close()
        conn.close()
        print("✅ Tables created successfully!")
    except Exception as e:
        print("Error creating tables:", e)

if __name__ == '__main__':
    init_tables()
