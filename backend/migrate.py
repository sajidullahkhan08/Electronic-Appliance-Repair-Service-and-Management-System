"""
migrate.py — Run this once to update the status column to VARCHAR
so it can hold both Shop Repair and Home Service specific statuses.
Usage: python migrate.py
"""

import pymysql
from config import Config


def migrate():
    conn = pymysql.connect(
        host=Config.MYSQL_HOST,
        port=Config.MYSQL_PORT,
        user=Config.MYSQL_USER,
        password=Config.MYSQL_PASSWORD,
        database=Config.MYSQL_DB,
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    with conn.cursor() as cur:
        cur.execute("""
            ALTER TABLE repair_requests
            MODIFY COLUMN status VARCHAR(50) NOT NULL DEFAULT 'Pending'
        """)
        conn.commit()
    conn.close()
    print("[OK] Migration complete: status column changed to VARCHAR(50).")


if __name__ == '__main__':
    migrate()
