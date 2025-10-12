-- ASSIGNMENT 1 QUERIES (10 Total)

-- 1. Number of orders per customer (Top 10)
SELECT customer_id, COUNT(order_id) AS total_orders
FROM orders
GROUP BY customer_id
ORDER BY total_orders DESC
    LIMIT 10;

-- 2. Top 10 products by total revenue
SELECT oi.product_id, SUM(oi.price) AS total_revenue
FROM order_items oi
GROUP BY oi.product_id
ORDER BY total_revenue DESC
    LIMIT 10;

-- 3. Payment type distribution
SELECT payment_type, COUNT(*) AS total_payments
FROM payments
GROUP BY payment_type
ORDER BY total_payments DESC;

-- 4. Average review score per seller
SELECT oi.seller_id, ROUND(AVG(r.review_score), 2) AS avg_score
FROM reviews r
         JOIN orders o ON r.order_id = o.order_id
         JOIN order_items oi ON o.order_id = oi.order_id
GROUP BY oi.seller_id
ORDER BY avg_score DESC
    LIMIT 10;

-- 5. Orders by state
SELECT c.customer_state, COUNT(o.order_id) AS total_orders
FROM orders o
         JOIN customers c ON o.customer_id = c.customer_id
GROUP BY c.customer_state
ORDER BY total_orders DESC;

-- 6. Most active sellers by number of items sold
SELECT seller_id, COUNT(order_item_id) AS items_sold
FROM order_items
GROUP BY seller_id
ORDER BY items_sold DESC
    LIMIT 10;

-- 7. Freight cost share of total price
SELECT ROUND(AVG(freight_value / NULLIF(price,0)), 2) AS avg_freight_share
FROM order_items
WHERE price > 0;

-- 8. Orders per month
SELECT DATE_TRUNC('month', order_purchase_timestamp) AS month,
       COUNT(*) AS total_orders
FROM orders
GROUP BY month
ORDER BY month;

-- 9. Average delivery delay (delivered - estimated) in days
SELECT ROUND(AVG(EXTRACT(EPOCH FROM (order_delivered_customer_date - order_estimated_delivery_date)) / 86400), 2)
           AS avg_delay_days
FROM orders
WHERE order_status = 'delivered'
  AND order_delivered_customer_date IS NOT NULL
  AND order_estimated_delivery_date IS NOT NULL;

-- 10. Correlation between review score and delivery time
SELECT r.review_score,
       ROUND(AVG(EXTRACT(EPOCH FROM (o.order_delivered_customer_date - o.order_purchase_timestamp)) / 86400), 2)
           AS avg_delivery_days
FROM reviews r
         JOIN orders o ON r.order_id = o.order_id
WHERE o.order_status = 'delivered'
  AND o.order_delivered_customer_date IS NOT NULL
  AND o.order_purchase_timestamp IS NOT NULL
GROUP BY r.review_score
ORDER BY r.review_score;


-- ASSIGNMENT 2 QUERIES (Visualization)


-- Q1: Top 10 states by number of customers (Pie Chart)
SELECT customer_state, COUNT(*) AS num_customers
FROM customers
GROUP BY customer_state
ORDER BY num_customers DESC
    LIMIT 10;

-- Q2: Top 10 product categories by total revenue (Bar Chart)
SELECT p.product_category, SUM(oi.price) AS total_revenue
FROM order_items oi
         JOIN products p ON oi.product_id = p.product_id
GROUP BY p.product_category
ORDER BY total_revenue DESC
    LIMIT 8;

-- Q3: Monthly revenue trend (Line Chart) — changed to LEFT JOIN
SELECT DATE_TRUNC('month', o.order_purchase_timestamp) AS month,
       SUM(oi.price) AS monthly_revenue
FROM orders o
    LEFT JOIN order_items oi ON o.order_id = oi.order_id
GROUP BY month
ORDER BY month;

-- Q4: Top 10 sellers by revenue (Horizontal Bar Chart) — changed to RIGHT JOIN
SELECT s.seller_id, SUM(oi.price) AS total_revenue
FROM order_items oi
         RIGHT JOIN sellers s ON oi.seller_id = s.seller_id
GROUP BY s.seller_id
ORDER BY total_revenue DESC
    LIMIT 10;

-- Q5: Distribution of review scores (Histogram)
SELECT CAST(review_score AS INTEGER) AS review_score
FROM order_reviews
WHERE review_score IS NOT NULL;

-- Q6: Correlation of delivery time vs review score (Scatter Plot)
SELECT EXTRACT(DAY FROM (o.order_delivered_customer_date - o.order_purchase_timestamp)) AS delivery_days,
       CAST(r.review_score AS INTEGER) AS review_score
FROM orders o
         JOIN order_reviews r ON o.order_id = r.order_id
WHERE o.order_delivered_customer_date IS NOT NULL
  AND r.review_score IS NOT NULL;

-- Q7 (Optional, for Plotly Time Slider): Orders per month with customer count
SELECT DATE_TRUNC('month', o.order_purchase_timestamp) AS month,
       COUNT(o.order_id) AS total_orders,
       COUNT(DISTINCT o.customer_id) AS unique_customers
FROM orders o
GROUP BY month
ORDER BY month;
