import psycopg2
import pandas as pd
import re
import warnings
warnings.filterwarnings('ignore', message='pandas only supports SQLAlchemy')

# Database connection details
DB_CONFIG = {
    "dbname": "Urbancart",  # <- set to your exact DB name from pgAdmin
    "user": "postgres",
    "password": "0000",
    "host": "localhost",
    "port": 5432
}

def run_queries_from_file(sql_file):
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        print("✅ Connected to database")

        with open(sql_file, "r", encoding="utf-8") as f:
            sql_content = f.read()

        queries = [q.strip() for q in sql_content.split(";") if q.strip()]

        for i, query in enumerate(queries, start=1):
            query_clean = re.sub(r'--.*\n', '', query)  # remove comments
            if query_clean.strip():
                print(f"\n--- Query {i} ---")
                try:
                    df = pd.read_sql(query_clean, conn)
                    print(df.head(10))
                except Exception as qe:
                    print(f"⚠️ Error running Query {i}: {qe}")

        conn.close()
        print("\n✅ Done")

    except Exception as e:
        print("❌ Error:", e)

if __name__ == "__main__":
    run_queries_from_file("queries.sql")
