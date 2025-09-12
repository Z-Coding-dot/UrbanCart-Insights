import psycopg2
import pandas as pd

# Database connection details
DB_CONFIG = {
    "dbname": "Urbancart",     
    "user": "postgres",     
    "password": "0000",
    "host": "localhost",   
    "port": 5432
}

# Define queries
QUERIES = {
    "orders_per_customer": """
        SELECT customer_id, COUNT(order_id) AS total_orders
        FROM orders
        GROUP BY customer_id
        ORDER BY total_orders DESC
        LIMIT 5;
    """,
    "top_products": """
        SELECT oi.product_id, SUM(oi.price) AS total_revenue
        FROM order_items oi
        GROUP BY oi.product_id
        ORDER BY total_revenue DESC
        LIMIT 5;
    """,
    "orders_per_month": """
        SELECT DATE_TRUNC('month', order_purchase_timestamp) AS month,
               COUNT(*) AS total_orders
        FROM orders
        GROUP BY month
        ORDER BY month
        LIMIT 5;
    """
}

def run_queries():
    try:
        # Connect to PostgreSQL
        conn = psycopg2.connect(**DB_CONFIG)
        print("✅ Connected to database")

        for name, query in QUERIES.items():
            print(f"\n--- {name} ---")
            df = pd.read_sql(query, conn)
            print(df)

        conn.close()
        print("\n✅ Done")

    except Exception as e:
        print("❌ Error:", e)

if __name__ == "__main__":
    run_queries()
