"""
init_db.py — Run this ONCE to set up the database, tables, and default admin.
Usage: python init_db.py
"""

from dotenv import load_dotenv

load_dotenv()

from werkzeug.security import generate_password_hash
from config import Config
from db import get_connection


def init():
    conn = get_connection(database=None)

    with conn.cursor() as cur:
        db_name = Config.MYSQL_DB
        cur.execute(f"CREATE DATABASE IF NOT EXISTS `{db_name}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
        conn.commit()

        # Use the configured database for schema execution
        cur.execute(f"USE `{db_name}`")

        # Read and execute schema
        with open('database/schema.sql', 'r', encoding='utf-8') as f:
            sql_script = f.read()

        # Execute each statement separately
        for statement in sql_script.split(';'):
            stmt = statement.strip()
            if stmt:
                cur.execute(stmt)

        conn.commit()

        # Check if admin already exists
        cur.execute("SELECT admin_id FROM admins WHERE username = %s", ('admin',))
        if not cur.fetchone():
            hashed = generate_password_hash('admin123')
            cur.execute(
                "INSERT INTO admins (username, password_hash) VALUES (%s, %s)",
                ('admin', hashed)
            )
            conn.commit()
            print("[OK] Default admin created  ->  username: admin  |  password: admin123")
        else:
            print("[INFO] Admin already exists, skipping seed.")

    conn.close()
    print("[OK] Database initialised successfully!")
    print("   DB:", Config.MYSQL_DB, "  |  Host:", Config.MYSQL_HOST, "  |  Port:", Config.MYSQL_PORT)

if __name__ == '__main__':
    init()
