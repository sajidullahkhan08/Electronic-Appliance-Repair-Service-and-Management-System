"""
routes/auth.py — Admin session authentication decorator.
"""

from functools import wraps
from flask import session, jsonify


def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('admin_logged_in'):
            return jsonify({'success': False, 'error': 'Unauthorized. Please log in.'}), 401
        return f(*args, **kwargs)
    return decorated
