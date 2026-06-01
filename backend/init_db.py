"""
init_db.py — Run this ONCE to set up the database, tables, and default admin.
Usage: python init_db.py
"""

import pymysql
from werkzeug.security import generate_password_hash
from config import Config

def init():
    # Connect without specifying the DB first
    conn = pymysql.connect(
        host=Config.MYSQL_HOST,
        port=Config.MYSQL_PORT,
        user=Config.MYSQL_USER,
        password=Config.MYSQL_PASSWORD,
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

    with conn.cursor() as cur:
        # Read and execute schema
        with open('database/schema.sql', 'r', encoding='utf-8') as f:
            sql_script = f.read()

        # Execute each statement separately
        for statement in sql_script.split(';'):
            stmt = statement.strip()
            if stmt:
                cur.execute(stmt)

        conn.commit()

        # Switch to the created database
        cur.execute("USE electrofix_db")

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
    print("   DB: electrofix_db  |  Host:", Config.MYSQL_HOST, "  |  Port:", Config.MYSQL_PORT)

if __name__ == '__main__':
    init()
