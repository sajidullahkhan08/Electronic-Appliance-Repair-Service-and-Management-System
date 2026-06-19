"""
models/repair_request.py — Repair request database operations.
"""

import secrets
import string
from db import get_db

# Status sets per service type
SHOP_STATUSES = ['Pending', 'Under Inspection', 'Repairing', 'Completed', 'Ready for Pickup']
HOME_STATUSES = ['Pending', 'Scheduled', 'Technician Dispatched', 'Repairing', 'Completed']
ALL_VALID_STATUSES = list(set(SHOP_STATUSES + HOME_STATUSES))


def generate_tracking_id():
    chars = string.ascii_uppercase + string.digits
    return 'EF' + ''.join(secrets.choice(chars) for _ in range(6))


def create_request(customer_id, appliance_type, appliance_brand,
                   problem_description, service_type):
    conn = get_db()
    try:
        # Ensure unique tracking ID
        while True:
            tid = generate_tracking_id()
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT request_id FROM repair_requests WHERE tracking_id = %s",
                    (tid,)
                )
                if not cur.fetchone():
                    break

        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO repair_requests
                    (tracking_id, customer_id, appliance_type, appliance_brand,
                     problem_description, service_type)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (tid, customer_id, appliance_type, appliance_brand,
                  problem_description, service_type))
            conn.commit()
            return tid
    finally:
        conn.close()


def get_request_by_tracking_id(tracking_id):
    conn = get_db()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT r.*, c.name AS customer_name, c.phone, c.address
                FROM repair_requests r
                JOIN customers c ON r.customer_id = c.customer_id
                WHERE r.tracking_id = %s
            """, (tracking_id.upper(),))
            return cur.fetchone()
    finally:
        conn.close()


def get_all_requests(service_type_filter=None):
    conn = get_db()
    try:
        with conn.cursor() as cur:
            if service_type_filter:
                cur.execute("""
                    SELECT
                        r.request_id          AS request_id,
                        r.tracking_id         AS tracking_id,
                        r.customer_id         AS customer_id,
                        r.appliance_type      AS appliance_type,
                        r.appliance_brand     AS appliance_brand,
                        r.problem_description AS problem_description,
                        r.service_type        AS service_type,
                        r.status              AS status,
                        r.notes               AS notes,
                        r.request_date        AS request_date,
                        r.updated_at          AS updated_at,
                        c.name                 AS customer_name,
                        c.phone                AS phone,
                        c.address              AS address
                    FROM repair_requests r
                    JOIN customers c ON r.customer_id = c.customer_id
                    WHERE r.service_type = %s
                    ORDER BY r.request_date DESC
                """, (service_type_filter,))
            else:
                cur.execute("""
                    SELECT
                        r.request_id          AS request_id,
                        r.tracking_id         AS tracking_id,
                        r.customer_id         AS customer_id,
                        r.appliance_type      AS appliance_type,
                        r.appliance_brand     AS appliance_brand,
                        r.problem_description AS problem_description,
                        r.service_type        AS service_type,
                        r.status              AS status,
                        r.notes               AS notes,
                        r.request_date        AS request_date,
                        r.updated_at          AS updated_at,
                        c.name                 AS customer_name,
                        c.phone                AS phone,
                        c.address              AS address
                    FROM repair_requests r
                    JOIN customers c ON r.customer_id = c.customer_id
                    ORDER BY r.request_date DESC
                """)
            return cur.fetchall()
    finally:
        conn.close()


def get_request_by_id(request_id):
    conn = get_db()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT r.*, c.name AS customer_name, c.phone, c.address
                FROM repair_requests r
                JOIN customers c ON r.customer_id = c.customer_id
                WHERE r.request_id = %s
            """, (request_id,))
            return cur.fetchone()
    finally:
        conn.close()


def update_status(request_id, status, notes=None):
    conn = get_db()
    try:
        # Normalize notes to empty string so SQL never sets NULL unintentionally
        if notes is None:
            notes = ''

        with conn.cursor() as cur:
            cur.execute(
                """
                UPDATE repair_requests
                SET status = %s,
                    notes = %s,
                    updated_at = CURRENT_TIMESTAMP
                WHERE request_id = %s
                """,
                (status, notes, request_id),
            )
            conn.commit()
            return cur.rowcount > 0
    finally:
        conn.close()



def get_dashboard_stats():
    conn = get_db()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) AS total FROM repair_requests")
            total = cur.fetchone()['total']

            cur.execute(
                "SELECT COUNT(*) AS cnt FROM repair_requests WHERE status = 'Pending'"
            )
            pending = cur.fetchone()['cnt']

            cur.execute(
                "SELECT COUNT(*) AS cnt FROM repair_requests WHERE status = 'Completed'"
            )
            completed = cur.fetchone()['cnt']

            cur.execute(
                "SELECT COUNT(*) AS cnt FROM repair_requests WHERE service_type = 'Home Service'"
            )
            home_services = cur.fetchone()['cnt']

            cur.execute(
                "SELECT COUNT(*) AS cnt FROM repair_requests WHERE status = 'Repairing'"
            )
            in_progress = cur.fetchone()['cnt']

            cur.execute("SELECT COUNT(*) AS cnt FROM customers")
            customers = cur.fetchone()['cnt']

            return {
                'total': total,
                'pending': pending,
                'completed': completed,
                'home_services': home_services,
                'in_progress': in_progress,
                'customers': customers
            }
    finally:
        conn.close()


def search_by_contact(query):
    """Search repair requests by customer name or phone number."""
    conn = get_db()
    try:
        with conn.cursor() as cur:
            like = f'%{query}%'
            cur.execute("""
                SELECT r.*, c.name AS customer_name, c.phone, c.address
                FROM repair_requests r
                JOIN customers c ON r.customer_id = c.customer_id
                WHERE c.name LIKE %s OR c.phone LIKE %s
                ORDER BY r.request_date DESC
                LIMIT 20
            """, (like, like))
            return cur.fetchall()
    finally:
        conn.close()
