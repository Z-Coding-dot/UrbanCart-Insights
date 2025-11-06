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

![Examples From queries & Analytical Topics](/charts/orders_per_month.png)
![Examples From queries & Analytical Topics](/charts/price_vs_freight.png)
![Examples From queries & Analytical Topics](/images/diagram.png)
![Examples From queries & Analytical Topics](/images/7.png)


---

# Prometheus + Grafana Monitoring Project

## Overview

This project demonstrates **real-time system and data monitoring** using **Prometheus** and **Grafana**.
Three separate dashboards were built to visualize and alert on metrics from:

1. **PostgreSQL Database Exporter**
2. **Node Exporter (System Metrics)**
3. **Custom Exporter (Weather API)**

---

## 1. Database Exporter (PostgreSQL)

**Purpose:** Monitor database performance and activity.
**Metrics visualized:**

* Number of active connections
* Database size (GB)
* Query per second (QPS)
* Uptime
* Read/write rate
* Number of users and tables

**Alert:**
Triggers when active connections > 50.

**Filter:**
`database` (selects monitored database).

---

## 2. Node Exporter (System Metrics)

**Purpose:** Track system resource usage in real time.
**Metrics visualized:**

* CPU usage per core
* Load average (1, 5, 15 min)
* Memory usage (total, used, free)
* Disk I/O
* Network traffic (in/out)
* System uptime

**Alert:**
Triggers when CPU usage > 80%.

**Filter:**
`instance` (monitored system node).

---

## 3. Custom Exporter (Weather API)

**Purpose:** Collect and expose live weather data from OpenWeather API using a custom Python exporter.
**Metrics visualized:**

* Temperature (°C)
* Humidity (%)
* Pressure (hPa)
* Wind speed (m/s)
* Cloudiness (%)
* Temperature difference (feels_like − actual)
* Sunrise / Sunset

**Alert:**
Triggers when temperature < −10°C or > 35°C.

**Filter:**
`city` (Astana, Almaty, London).

---

## Tools and Configuration

* **Prometheus** – metrics collection
* **Grafana** – dashboards and alerting
* **Docker Compose** – runs Prometheus, Grafana, and exporters
* **custom_exporter.py** – Python script exposing metrics on port 8010
* **prometheus.yml** – Prometheus scrape configuration

---

## Files in Repository

* `docker-compose.yml`
* `prometheus.yml`
* `custom_exporter.py`
* `README.md`
* `dashboards/` (exported JSON files of all 3 dashboards)

---

## How to Run

1. Start all containers:

   ```bash
   docker compose up -d
   ```
2. Run the Python exporter:

   ```bash
   python custom_exporter.py
   ```
3. Open Grafana → `http://localhost:3000`
4. Explore dashboards and confirm all targets show **UP** in Prometheus.



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

---

## Assignment 2 - Visualizations & Export

This repository includes Assignment #2 deliverables built on the UrbanCart database.

What gets generated when you run `python main.py`:
- 6 charts saved to `charts/` with titles/labels/legend where applicable:
  - `payment_pie.png` — Distribution of payment types (JOIN with orders/customers)
  - `top_products_bar.png` — Top 10 product categories by revenue (delivered)
  - `orders_state_barh.png` — Orders by customer state (paid orders)
  - `orders_per_month.png` — Monthly revenue trend (delivered)
  - `review_scores_histogram.png` — Distribution of review scores
  - `price_vs_freight.png` — Product price vs freight cost scatter
- Plotly time-slider demo (interactive window): Orders over time by year
- Formatted Excel export saved to `exports/report.xlsx` with:
  - Frozen header (`B2`), filters on all columns
  - Numeric columns with a 3-color gradient scale
  - Console summary: file name, sheet count, total rows

Notes:
- If your `reviews` table is empty, the script seeds a few synthetic reviews (delivered orders) for demo purposes so the histogram is not empty.
- All data is loaded from PostgreSQL via SQL queries; queries use JOINs and meaningful business aggregations.

Demo flow for defense:
1. Run: `python main.py` to generate charts and open the Plotly slider.
2. Insert/update a row (use your own insert or the included seeding), then rerun the relevant chart function by re-running the script to show the update reflected.



---

**Author:** Parsa Karimi
**Course:** Data Visualization — 2025/11/6
