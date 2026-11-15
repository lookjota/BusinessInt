-- SQLite queries. Run: sqlite3 -header -column outputs/sales.sqlite < sql/analysis.sql
-- Only completed orders appear in sales_clean.

-- 1. Revenue and average ticket
SELECT ROUND(SUM(revenue), 2) AS total_revenue_brl,
       COUNT(DISTINCT order_id) AS completed_orders,
       ROUND(SUM(revenue) / NULLIF(COUNT(DISTINCT order_id), 0), 2) AS avg_order_value_brl
FROM sales_clean;

-- 2. Revenue by month
SELECT substr(order_date, 1, 7) AS month, ROUND(SUM(revenue), 2) AS revenue_brl
FROM sales_clean GROUP BY 1 ORDER BY 1;

-- 3. Top products
SELECT product_name, SUM(quantity) AS units, ROUND(SUM(revenue), 2) AS revenue_brl
FROM sales_clean GROUP BY product_name ORDER BY revenue_brl DESC LIMIT 5;

-- 4. Revenue by region
SELECT region, ROUND(SUM(revenue), 2) AS revenue_brl
FROM sales_clean GROUP BY region ORDER BY revenue_brl DESC;

-- 5. Monthly revenue growth using a window function
WITH monthly AS (
  SELECT substr(order_date, 1, 7) AS month, SUM(revenue) AS revenue
  FROM sales_clean GROUP BY 1
), growth AS (
  SELECT month, revenue, LAG(revenue) OVER (ORDER BY month) AS previous_revenue
  FROM monthly
)
SELECT month, ROUND(revenue, 2) AS revenue_brl,
       ROUND(100.0 * (revenue - previous_revenue) / NULLIF(previous_revenue, 0), 2) AS mom_growth_pct
FROM growth ORDER BY month;
