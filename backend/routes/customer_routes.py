"""
routes/customer_routes.py — Public customer-facing API endpoints.
"""

from flask import Blueprint, request, jsonify
from models.customer import create_or_get_customer
from models.repair_request import (
    create_request, get_request_by_tracking_id,
    search_by_contact, SHOP_STATUSES, HOME_STATUSES
)

customer_bp = Blueprint('customer', __name__)

VALID_APPLIANCES = [
    'Washing Machine', 'Freezer', 'Refrigerator', 'Stabilizer',
    'Electric Iron', 'Water Dispenser', 'Fan', 'Microwave Oven', 'Other'
]
VALID_SERVICE_TYPES = ['Home Service', 'Shop Repair']


@customer_bp.route('/request', methods=['POST'])
def submit_request():
    data = request.get_json()

    # --- Validation ---
    required = ['name', 'phone', 'appliance_type', 'problem_description', 'service_type']
    for field in required:
        if not data.get(field, '').strip():
            return jsonify({'success': False, 'error': f'Field "{field}" is required.'}), 400

    if data['appliance_type'] not in VALID_APPLIANCES:
        return jsonify({'success': False, 'error': 'Invalid appliance type.'}), 400

    if data['service_type'] not in VALID_SERVICE_TYPES:
        return jsonify({'success': False, 'error': 'Invalid service type.'}), 400

    if data['service_type'] == 'Home Service' and not data.get('address', '').strip():
        return jsonify({'success': False, 'error': 'Address is required for Home Service.'}), 400

    try:
        customer_id = create_or_get_customer(
            name=data['name'].strip(),
            phone=data['phone'].strip(),
            address=data.get('address', '').strip()
        )
        tracking_id = create_request(
            customer_id=customer_id,
            appliance_type=data['appliance_type'],
            appliance_brand=data.get('appliance_brand', '').strip(),
            problem_description=data['problem_description'].strip(),
            service_type=data['service_type']
        )
        return jsonify({'success': True, 'tracking_id': tracking_id}), 201

    except Exception as e:
        return jsonify({'success': False, 'error': 'Server error. Please try again.'}), 500


@customer_bp.route('/track/<tracking_id>', methods=['GET'])
def track_request(tracking_id):
    if not tracking_id:
        return jsonify({'success': False, 'error': 'Tracking ID is required.'}), 400

    result = get_request_by_tracking_id(tracking_id)
    if not result:
        return jsonify({'success': False, 'error': 'No record found for this Tracking ID.'}), 404

    # Serialize datetime fields
    data = dict(result)
    if data.get('request_date'):
        data['request_date'] = data['request_date'].strftime('%d %b %Y, %I:%M %p')
    if data.get('updated_at'):
        data['updated_at'] = data['updated_at'].strftime('%d %b %Y, %I:%M %p')

    return jsonify({'success': True, 'data': data}), 200


@customer_bp.route('/track-by-contact', methods=['GET'])
def track_by_contact():
    """Search repair requests by customer name or phone number."""
    query = request.args.get('query', '').strip()
    if not query or len(query) < 3:
        return jsonify({'success': False, 'error': 'Enter at least 3 characters to search.'}), 400

    results = search_by_contact(query)
    if not results:
        return jsonify({'success': False, 'error': 'No repair records found for that name or phone number.'}), 404

    serialized = []
    for r in results:
        row = dict(r)
        if row.get('request_date'):
            row['request_date'] = row['request_date'].strftime('%d %b %Y, %I:%M %p')
        if row.get('updated_at'):
            row['updated_at'] = row['updated_at'].strftime('%d %b %Y, %I:%M %p')
        serialized.append(row)

    return jsonify({'success': True, 'data': serialized}), 200
