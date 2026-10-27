CREATE TABLE dim_customers (
    customer_id INT PRIMARY KEY
);

CREATE TABLE dim_products (
    product_id SERIAL PRIMARY KEY,
    product_name VARCHAR(255) UNIQUE
);

CREATE TABLE fact_sales (
    sale_id SERIAL PRIMARY KEY,
    customer_id INT REFERENCES dim_customers(customer_id),
    product_id INT REFERENCES dim_products(product_id),
    quantity INT,
    price DECIMAL(10, 2),
    total_amount DECIMAL(10, 2),
    order_date TIMESTAMP
);

INSERT INTO dim_customers (customer_id)
SELECT DISTINCT customer_id 
FROM orders 
WHERE customer_id IS NOT NULL
ON CONFLICT (customer_id) DO NOTHING;

INSERT INTO dim_products (product_name)
SELECT DISTINCT product_name 
FROM orders 
WHERE product_name IS NOT NULL
ON CONFLICT (product_name) DO NOTHING;

INSERT INTO fact_sales (customer_id, product_id, quantity, price, total_amount, order_date)
SELECT 
    o.customer_id,
    p.product_id,
    o.quantity,
    o.price,
    (o.quantity * o.price) AS total_amount,
    o.order_date
FROM orders o
JOIN dim_products p ON o.product_name = p.product_name;