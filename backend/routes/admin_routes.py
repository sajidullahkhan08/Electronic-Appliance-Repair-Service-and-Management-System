"""
routes/admin_routes.py — Admin-only API endpoints (session-protected).
"""

from flask import Blueprint, request, jsonify, session
from routes.auth import admin_required
from models.admin import verify_admin, update_admin_password
from models.repair_request import (
    get_all_requests, get_request_by_id, update_status, get_dashboard_stats,
    ALL_VALID_STATUSES, SHOP_STATUSES, HOME_STATUSES
)
from models.customer import get_all_customers, get_customer_by_id, get_customer_history

admin_bp = Blueprint('admin', __name__)

VALID_STATUSES = ALL_VALID_STATUSES


# ── Auth ─────────────────────────────────────────────────────────────────────

@admin_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username', '').strip()
    password = data.get('password', '')

    if not username or not password:
        return jsonify({'success': False, 'error': 'Username and password required.'}), 400

    admin = verify_admin(username, password)
    if not admin:
        return jsonify({'success': False, 'error': 'Invalid credentials.'}), 401

    session.permanent = True
    session['admin_logged_in'] = True
    session['admin_id'] = admin['admin_id']
    session['admin_username'] = admin['username']

    return jsonify({'success': True, 'username': admin['username']}), 200


@admin_bp.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'success': True}), 200


@admin_bp.route('/check-auth', methods=['GET'])
def check_auth():
    if session.get('admin_logged_in'):
        return jsonify({'authenticated': True, 'username': session.get('admin_username')}), 200
    return jsonify({'authenticated': False}), 200


# ── Dashboard ─────────────────────────────────────────────────────────────────

@admin_bp.route('/stats', methods=['GET'])
@admin_required
def stats():
    data = get_dashboard_stats()
    return jsonify({'success': True, 'data': data}), 200


# ── Repair Requests ───────────────────────────────────────────────────────────

@admin_bp.route('/requests', methods=['GET'])
@admin_required
def all_requests():
    service_filter = request.args.get('service_type')
    rows = get_all_requests(service_filter)
    result = []
    for r in rows:
        row = dict(r)
        if row.get('request_date'):
            row['request_date'] = row['request_date'].strftime('%d %b %Y, %I:%M %p')
        if row.get('updated_at'):
            row['updated_at'] = row['updated_at'].strftime('%d %b %Y, %I:%M %p')
        result.append(row)
    return jsonify({'success': True, 'data': result}), 200


@admin_bp.route('/requests/<int:request_id>', methods=['GET'])
@admin_required
def single_request(request_id):
    row = get_request_by_id(request_id)
    if not row:
        return jsonify({'success': False, 'error': 'Request not found.'}), 404
    data = dict(row)
    if data.get('request_date'):
        data['request_date'] = data['request_date'].strftime('%d %b %Y, %I:%M %p')
    if data.get('updated_at'):
        data['updated_at'] = data['updated_at'].strftime('%d %b %Y, %I:%M %p')
    return jsonify({'success': True, 'data': data}), 200


@admin_bp.route('/requests/<int:request_id>/status', methods=['PUT'])
@admin_required
def update_request_status(request_id):
    data = request.get_json()
    status = data.get('status', '')
    notes = data.get('notes', '')

    if status not in VALID_STATUSES:
        return jsonify({'success': False, 'error': 'Invalid status value.'}), 400

    ok = update_status(request_id, status, notes)
    if not ok:
        return jsonify({'success': False, 'error': 'Request not found.'}), 404

    return jsonify({'success': True, 'message': 'Status updated successfully.'}), 200


# ── Customers ─────────────────────────────────────────────────────────────────

@admin_bp.route('/customers', methods=['GET'])
@admin_required
def all_customers():
    rows = get_all_customers()
    result = []
    for r in rows:
        row = dict(r)
        if row.get('created_at'):
            row['created_at'] = row['created_at'].strftime('%d %b %Y')
        result.append(row)
    return jsonify({'success': True, 'data': result}), 200


@admin_bp.route('/customers/<int:customer_id>', methods=['GET'])
@admin_required
def customer_detail(customer_id):
    customer = get_customer_by_id(customer_id)
    if not customer:
        return jsonify({'success': False, 'error': 'Customer not found.'}), 404
    history = get_customer_history(customer_id)
    serialized = []
    for h in history:
        row = dict(h)
        if row.get('request_date'):
            row['request_date'] = row['request_date'].strftime('%d %b %Y, %I:%M %p')
        serialized.append(row)
    c = dict(customer)
    if c.get('created_at'):
        c['created_at'] = c['created_at'].strftime('%d %b %Y')
    return jsonify({'success': True, 'data': c, 'history': serialized}), 200


# ── Home Services ─────────────────────────────────────────────────────────────

@admin_bp.route('/home-services', methods=['GET'])
@admin_required
def home_services():
    rows = get_all_requests(service_type_filter='Home Service')
    result = []
    for r in rows:
        row = dict(r)
        if row.get('request_date'):
            row['request_date'] = row['request_date'].strftime('%d %b %Y, %I:%M %p')
        if row.get('updated_at'):
            row['updated_at'] = row['updated_at'].strftime('%d %b %Y, %I:%M %p')
        result.append(row)
    return jsonify({'success': True, 'data': result}), 200


@admin_bp.route('/status-options', methods=['GET'])
@admin_required
def status_options():
    """Return appropriate status list for a given service type."""
    stype = request.args.get('service_type', 'Shop Repair')
    statuses = HOME_STATUSES if stype == 'Home Service' else SHOP_STATUSES
    return jsonify({'success': True, 'statuses': statuses}), 200


# ── Password Change ───────────────────────────────────────────────────────────

@admin_bp.route('/change-password', methods=['PUT'])
@admin_required
def change_password():
    """Allow the logged-in admin to set a new password."""
    data = request.get_json()
    new_password    = data.get('new_password', '').strip()
    confirm_password = data.get('confirm_password', '').strip()

    if not new_password:
        return jsonify({'success': False, 'error': 'New password cannot be empty.'}), 400

    if len(new_password) < 6:
        return jsonify({'success': False, 'error': 'Password must be at least 6 characters.'}), 400

    if new_password != confirm_password:
        return jsonify({'success': False, 'error': 'Passwords do not match.'}), 400

    admin_id = session.get('admin_id')
    ok = update_admin_password(admin_id, new_password)

    if ok:
        return jsonify({'success': True, 'message': 'Password updated successfully.'}), 200
    return jsonify({'success': False, 'error': 'Failed to update password.'}), 500
