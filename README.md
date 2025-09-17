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

![Examples From queries & Analytical Topics](/images/diagram.png)
![Examples From queries & Analytical Topics](/images/one.png)
![Examples From queries & Analytical Topics](/images/3.png)
![Examples From queries & Analytical Topics](/images/7.png)

---

## Setup Instructions

### Prerequisites
1. Install **PostgreSQL 17** and **Python 3.10+**
2. Install required Python packages:
   ```bash
   pip install psycopg2-binary pandas sqlalchemy
   ```

### Database Setup
1. **Run the setup script** (recommended):
   ```bash
   python setup_database.py
   ```
   
   OR manually:
   
2. Create a database called `urbancart`:
   ```sql
   createdb -U postgres urbancart
   ```

3. Run the schema file to create tables:
   ```bash
   psql -U postgres -d urbancart -f schema.sql
   ```

### Data Import
1. **Download the Olist dataset** from [Kaggle](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)
2. **Extract and rename** the CSV files to match these exact names:
   - `olist_customers_dataset.csv`
   - `olist_sellers_dataset.csv`
   - `olist_products_dataset.csv`
   - `olist_orders_dataset.csv`
   - `olist_order_items_dataset.csv`
   - `olist_order_payments_dataset.csv`
   - `olist_order_reviews_dataset.csv`
   - `olist_geolocation_dataset.csv`

3. **Import the data**:
   ```bash
   psql -U postgres -d urbancart -f import_instructions.sql
   ```

### Run the Analysis
```bash
python main.py
```

### Troubleshooting
- **"relation does not exist" errors**: Make sure you've run `schema.sql` and imported the CSV data
- **Connection errors**: Verify PostgreSQL is running and credentials are correct in `main.py`
- **Import errors**: Check that CSV files are in the correct directory and have the right names
