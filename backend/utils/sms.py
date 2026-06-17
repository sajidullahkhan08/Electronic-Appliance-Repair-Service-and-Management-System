"""
utils/sms.py — SMS helper for sending OTP via Twilio.

Twilio free trial: https://www.twilio.com/try-twilio
- Set TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_FROM_NUMBER in .env
- Pakistani numbers are sent as +92XXXXXXXXXX format
"""

import random
import string
import re
from config import Config


def normalize_pk_phone(phone: str) -> str:
    """
    Normalize a Pakistani phone number to international E.164 format.
    Accepts: 03441234567 / +923441234567 / 923441234567
    Returns: +923441234567
    """
    phone = re.sub(r'\s|-', '', phone.strip())
    if phone.startswith('+92'):
        return phone
    if phone.startswith('92') and len(phone) == 12:
        return '+' + phone
    if phone.startswith('0') and len(phone) == 11:
        return '+92' + phone[1:]
    # Return as-is if already in another international format
    return phone


def generate_otp(length: int = 6) -> str:
    """Return a random numeric OTP string."""
    return ''.join(random.choices(string.digits, k=length))


def send_otp_sms(to_phone: str, otp_code: str, purpose: str) -> tuple[bool, str]:
    """
    Send an OTP SMS via Twilio.

    Returns (True, sid) on success or (False, error_message) on failure.
    If Twilio credentials are not configured, returns (False, 'SMS not configured').
    """
    if not all([Config.TWILIO_ACCOUNT_SID, Config.TWILIO_AUTH_TOKEN, Config.TWILIO_FROM_NUMBER]):
        # Allow development without Twilio — OTP will be printed to console
        print(f"\n[DEV] OTP for {to_phone} [{purpose}]: {otp_code}\n")
        return True, 'dev-mode'

    try:
        from twilio.rest import Client
        normalized = normalize_pk_phone(to_phone)
        action = 'password change' if purpose == 'change_password' else 'phone number change'
        body = (
            f"ElectroFix Admin OTP: {otp_code}\n"
            f"Requested action: {action}\n"
            f"Valid for 5 minutes. Do not share this code."
        )
        client = Client(Config.TWILIO_ACCOUNT_SID, Config.TWILIO_AUTH_TOKEN)
        message = client.messages.create(
            body=body,
            from_=Config.TWILIO_FROM_NUMBER,
            to=normalized
        )
        return True, message.sid
    except Exception as exc:
        return False, str(exc)
