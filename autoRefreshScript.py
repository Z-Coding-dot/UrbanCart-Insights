
import psycopg2
import time
import uuid
from datetime import datetime, timedelta
import random

# --- DATABASE CONFIGURATION (REPLACE WITH YOUR DETAILS) ---
DB_NAME = "Urbancart"
DB_USER = "postgres"
DB_PASS = "0000"
DB_HOST = "localhost" # or 'host.docker.internal' if running script outside a docker network
DB_PORT = "5432"

# These are required to ensure the inserted data is "meaningful" and respects FK constraints.
EXISTING_CUSTOMER_ID = "00012a2ce6f8dcda20d059ce98491703" # Example existing Customer ID
EXISTING_SELLER_ID = "0015a82c2db000af6aaaf3ae2ecb0532"   # Example existing Seller ID
EXISTING_PRODUCT_ID = "00066f42aeeb9f3007548bb9d3f33c38"   # Example existing Product ID

# --- INSERT INTERVAL ---
INSERT_INTERVAL_SECONDS = 10  # Insert a new record every 10 seconds (between 5-20 seconds) [cite: 27]

def insert_new_order_data():
    """Generates and inserts a new order and order item into the database."""
    new_order_id = str(uuid.uuid4()).replace('-', '')  # Generate a unique Order ID
    current_timestamp = datetime.now()

    # 1. New Order Data (Base Transaction)
    order_data = (
        new_order_id,
        EXISTING_CUSTOMER_ID,
        'delivered', # Status must be valid
        current_timestamp, # purchase_timestamp
        current_timestamp + timedelta(hours=random.randint(1, 48)), # approved_at
        current_timestamp + timedelta(days=random.randint(1, 10)),  # estimated_delivery_date
    )

    # 2. New Order Item Data (Item detail)
    item_data = (
        new_order_id,
        1, # order_item_id
        EXISTING_PRODUCT_ID,
        EXISTING_SELLER_ID,
        random.uniform(10.00, 500.00), # price
        random.uniform(5.00, 50.00)     # freight_value
    )

    # SQL INSERT Statements
    order_sql = """
                INSERT INTO orders
                (order_id, customer_id, order_status, order_purchase_timestamp, order_approved_at, order_estimated_delivery_date)
                VALUES (%s, %s, %s, %s, %s, %s) \
                """

    item_sql = """
               INSERT INTO order_items
                   (order_id, order_item_id, product_id, seller_id, price, freight_value)
               VALUES (%s, %s, %s, %s, %s, %s) \
               """

    conn = None
    try:
        # Connect to the PostgreSQL database
        conn = psycopg2.connect(
            dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST, port=DB_PORT
        )
        cur = conn.cursor()

        # Execute the INSERTs
        cur.execute(order_sql, order_data)
        cur.execute(item_sql, item_data)

        # Commit the transaction
        conn.commit()
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Inserted new order: {new_order_id}")

        cur.close()

    except Exception as error:
        print(f"Error during database operation: {error}")
        if conn:
            conn.rollback()

    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    print("--- Starting Auto Data Refresh Script ---")
    print(f"Inserting new records every {INSERT_INTERVAL_SECONDS} seconds. Press Ctrl+C to stop.")

    while True:
        insert_new_order_data()
        time.sleep(INSERT_INTERVAL_SECONDS)