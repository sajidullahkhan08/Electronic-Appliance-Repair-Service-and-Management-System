"""
models/admin.py — Admin authentication operations.
"""

from db import get_db
from werkzeug.security import check_password_hash


def get_admin_by_username(username):
    conn = get_db()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT * FROM admins WHERE username = %s",
                (username,)
            )
            return cur.fetchone()
    finally:
        conn.close()


def verify_admin(username, password):
    """
    Returns admin dict on success, None on failure.
    """
    admin = get_admin_by_username(username)
    if admin and check_password_hash(admin['password_hash'], password):
        return admin
    return None
