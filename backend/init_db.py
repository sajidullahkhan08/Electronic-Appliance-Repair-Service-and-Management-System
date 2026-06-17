"""
init_db.py — Run ONCE to create the database, tables, and default admin.
Usage: python init_db.py
"""

from dotenv import load_dotenv
load_dotenv()

from werkzeug.security import generate_password_hash
from config import Config
from db import get_connection


# ── Default admin credentials (change after first login) ─────────────────────
DEFAULT_PHONE    = '+923279749220'   # Pakistani format — stored as-is
DEFAULT_PASSWORD = 'admin123'


def init():
    conn = get_connection(database=None)

    with conn.cursor() as cur:
        db_name = Config.MYSQL_DB
        cur.execute(
            f"CREATE DATABASE IF NOT EXISTS `{db_name}` "
            f"CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
        )
        conn.commit()
        cur.execute(f"USE `{db_name}`")

        # Read and execute schema
        with open('database/schema.sql', 'r', encoding='utf-8') as f:
            sql_script = f.read()

        for statement in sql_script.split(';'):
            stmt = statement.strip()
            if stmt:
                cur.execute(stmt)
        conn.commit()

        # Seed default admin if none exists
        cur.execute("SELECT admin_id FROM admins WHERE phone = %s", (DEFAULT_PHONE,))
        if not cur.fetchone():
            hashed = generate_password_hash(DEFAULT_PASSWORD)
            cur.execute(
                "INSERT INTO admins (phone, password_hash) VALUES (%s, %s)",
                (DEFAULT_PHONE, hashed)
            )
            conn.commit()
            print(f"[OK] Default admin created.")
            print(f"     Phone:    {DEFAULT_PHONE}")
            print(f"     Password: {DEFAULT_PASSWORD}")
        else:
            print("[INFO] Admin already exists — skipping seed.")

    conn.close()
    print("[OK] Database initialised successfully!")
    print(f"     DB: {Config.MYSQL_DB}  |  Host: {Config.MYSQL_HOST}  |  Port: {Config.MYSQL_PORT}")


if __name__ == '__main__':
    init()
