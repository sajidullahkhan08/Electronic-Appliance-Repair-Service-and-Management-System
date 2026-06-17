"""
models/otp.py — OTP creation and verification against the database.
"""

from datetime import datetime, timedelta
from db import get_db


VALID_PURPOSES = ('change_password', 'change_phone')


def create_otp(phone: str, code: str, purpose: str, expiry_minutes: int = 5) -> bool:
    """
    Invalidates any previous unused OTPs for this phone+purpose,
    then inserts a fresh OTP that expires in `expiry_minutes`.
    Returns True on success.
    """
    if purpose not in VALID_PURPOSES:
        return False

    conn = get_db()
    try:
        with conn.cursor() as cur:
            # Expire all previous unused OTPs for same phone + purpose
            cur.execute(
                "UPDATE otp_codes SET used = 1 WHERE phone = %s AND purpose = %s AND used = 0",
                (phone, purpose)
            )
            expires_at = datetime.now() + timedelta(minutes=expiry_minutes)
            cur.execute(
                "INSERT INTO otp_codes (phone, code, purpose, expires_at) VALUES (%s, %s, %s, %s)",
                (phone, code, purpose, expires_at)
            )
            conn.commit()
            return True
    except Exception:
        return False
    finally:
        conn.close()


def verify_otp(phone: str, code: str, purpose: str) -> bool:
    """
    Returns True if a matching, unexpired, unused OTP exists and marks it used.
    Returns False on any mismatch, expiry, or reuse attempt.
    """
    conn = get_db()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """SELECT otp_id FROM otp_codes
                   WHERE phone = %s AND code = %s AND purpose = %s
                     AND used = 0 AND expires_at > NOW()""",
                (phone, code, purpose)
            )
            row = cur.fetchone()
            if not row:
                return False
            # Mark as consumed — cannot be reused
            cur.execute(
                "UPDATE otp_codes SET used = 1 WHERE otp_id = %s",
                (row['otp_id'],)
            )
            conn.commit()
            return True
    except Exception:
        return False
    finally:
        conn.close()
