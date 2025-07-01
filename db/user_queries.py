# db/user_queries.py
import psycopg2
import os

def get_connection():
    return psycopg2.connect(
        dbname=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASS'),
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT')
    )

def create_user(username, hashed_password):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO "user" (username, password)
        VALUES (%s, %s)
        RETURNING id, username;
    """, (username, hashed_password))
    new_user = cursor.fetchone()
    conn.commit()
    cursor.close()
    conn.close()
    return new_user

def get_user_by_username(username):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, username, password
        FROM "user"
        WHERE username = %s;
    """, (username,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    return user
