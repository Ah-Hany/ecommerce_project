SELECT 
    product_name,
    SUM(quantity) AS total_quantity_sold,
    SUM(quantity * price) AS total_revenue
FROM orders
GROUP BY product_name
ORDER BY total_revenue DESC;

SELECT 
    DATE_TRUNC('month', order_date) AS order_month,
    COUNT(order_id) AS total_orders,
    SUM(quantity * price) AS monthly_sales
FROM orders
GROUP BY order_month
ORDER BY order_month DESC;

SELECT 
    customer_id,
    COUNT(order_id) AS order_count,
    SUM(quantity * price) AS total_spent
FROM orders
GROUP BY customer_id
ORDER BY total_spent DESC;