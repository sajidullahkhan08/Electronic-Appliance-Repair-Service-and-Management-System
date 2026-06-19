"""
migrate.py — Run this once to update the status column to VARCHAR
so it can hold both Shop Repair and Home Service specific statuses.
Usage: python migrate.py
"""

from dotenv import load_dotenv

load_dotenv()

from config import Config
from db import get_db


def migrate():
    conn = get_db()
    with conn.cursor() as cur:
        cur.execute("""
            ALTER TABLE repair_requests
            MODIFY COLUMN status VARCHAR(50) NOT NULL DEFAULT 'Pending'
        """)
        # Repair rows left empty by the old ENUM rejecting home-service statuses
        cur.execute("""
            UPDATE repair_requests
            SET status = 'Pending'
            WHERE status IS NULL OR status = ''
        """)
        conn.commit()
    conn.close()
    print("[OK] Migration complete: status column changed to VARCHAR(50).")
    print("[OK] Empty status values reset to 'Pending'.")


if __name__ == '__main__':
    migrate()
