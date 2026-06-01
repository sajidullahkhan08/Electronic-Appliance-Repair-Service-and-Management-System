"""
models/customer.py — Customer database operations.
"""

from db import get_db


def create_or_get_customer(name, phone, address):
    """
    Find existing customer by phone or create a new one.
    Returns customer_id.
    """
    conn = get_db()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT customer_id FROM customers WHERE phone = %s",
                (phone,)
            )
            row = cur.fetchone()
            if row:
                return row['customer_id']

            cur.execute(
                "INSERT INTO customers (name, phone, address) VALUES (%s, %s, %s)",
                (name, phone, address)
            )
            conn.commit()
            return cur.lastrowid
    finally:
        conn.close()


def get_all_customers():
    conn = get_db()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT c.customer_id, c.name, c.phone, c.address, c.created_at,
                       COUNT(r.request_id) AS total_requests
                FROM customers c
                LEFT JOIN repair_requests r ON c.customer_id = r.customer_id
                GROUP BY c.customer_id
                ORDER BY c.created_at DESC
            """)
            return cur.fetchall()
    finally:
        conn.close()


def get_customer_by_id(customer_id):
    conn = get_db()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT * FROM customers WHERE customer_id = %s",
                (customer_id,)
            )
            return cur.fetchone()
    finally:
        conn.close()


def get_customer_history(customer_id):
    conn = get_db()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT * FROM repair_requests
                WHERE customer_id = %s
                ORDER BY request_date DESC
            """, (customer_id,))
            return cur.fetchall()
    finally:
        conn.close()
