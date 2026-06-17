"""
models/admin.py — Admin authentication and account management.
"""

from db import get_db
from werkzeug.security import check_password_hash, generate_password_hash


def get_admin_by_phone(phone: str) -> dict | None:
    """Return admin row for the given phone number, or None."""
    conn = get_db()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT * FROM admins WHERE phone = %s",
                (phone,)
            )
            return cur.fetchone()
    finally:
        conn.close()


def verify_admin(phone: str, password: str) -> dict | None:
    """
    Verify login credentials.
    Returns the admin dict on success, None on failure.
    """
    admin = get_admin_by_phone(phone)
    if admin and check_password_hash(admin['password_hash'], password):
        return admin
    return None


def update_admin_password(admin_id: int, new_password: str) -> bool:
    """
    Hash new_password and save it.
    Returns True on success, False if admin not found.
    """
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


def update_admin_phone(admin_id: int, new_phone: str) -> bool:
    """
    Update the admin's registered phone number.
    Returns True on success, False if admin not found or phone already used.
    """
    conn = get_db()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "UPDATE admins SET phone = %s WHERE admin_id = %s",
                (new_phone, admin_id)
            )
            conn.commit()
            return cur.rowcount > 0
    except Exception:
        # Phone unique constraint violation
        return False
    finally:
        conn.close()
