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


def update_admin_password(admin_id, new_password):
    """
    Hashes new_password and saves it for the given admin_id.
    Returns True on success, False if admin not found.
    """
    from werkzeug.security import generate_password_hash
    conn = get_db()
    try:
        with conn.cursor() as cur:
            hashed = generate_password_hash(new_password)
            cur.execute(
                "UPDATE admins SET password_hash = %s WHERE admin_id = %s",
                (hashed, admin_id)
            )
            conn.commit()
            return cur.rowcount > 0
    finally:
        conn.close()
