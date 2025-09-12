# UrbanCart Insights

## Company Overview
UrbanCart is an e-commerce retailer specializing in a wide variety of products across multiple regions.  
As a data analyst at UrbanCart, I focus on building a robust database to analyze customer behavior, sales performance, payments, reviews, and logistics.  
The analysis provides insights that help improve delivery efficiency, customer satisfaction, and overall revenue growth.

---

## Project Description
This project uses the **Olist Brazilian E-Commerce Public Dataset** (Kaggle), which contains over **100k orders** and multiple related tables.  
It is designed to simulate a real-world online retail environment with customers, sellers, products, orders, payments, reviews, and geolocation data.  

The goal of this project is to:
- Build a relational database in PostgreSQL.  
- Practice SQL joins, aggregations, and analytics on a large dataset.  
- Run Python scripts to execute queries and prepare data for future visualization.  

---

## Database Schema
The database contains the following main tables:

- **customers** → customer IDs, location (city/state, zip).  
- **orders** → purchase details, status, and timestamps.  
- **order_items** → product-level order breakdown with sellers, prices, and freight.  
- **products** → product catalog with category and dimensions.  
- **payments** → payment type, value, and installments per order.  
- **reviews** → customer feedback and review scores.  
- **sellers** → seller IDs, city, and state.  
- **geolocation** → mapping of zip codes to latitude/longitude.  

**Relationships:**
- Each `customer` can place many `orders`.  
- Each `order` can have multiple `order_items`, `payments`, and a `review`.  
- Each `order_item` links to a `product` and a `seller`.  
- `geolocation` helps map customers and sellers geographically.  

_ER diagram (to be added in `/images/one.png`)._

---

## Setup Instructions
1. Install **PostgreSQL 17** and **Python 3.10+**.  
2. Create a database called `urbancart`.  
3. Run the provided `schema.sql` file to create tables.  
4. Import CSVs using `\copy` in `psql` (see `import_instructions.sql`).  
5. Verify with sample queries from `queries.sql`.  
6. Run the Python script:  
   ```bash
   pip install psycopg2-binary pandas
   python main.py
