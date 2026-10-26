from datetime import datetime, timedelta
import random
import psycopg2

conn = psycopg2.connect(
    dbname="ecommerce_source",
    user="postgres",
    password="42024137",
    host="localhost",
    port="5432",
)
cur = conn.cursor()

cur.execute("""
    DROP TABLE IF EXISTS orders;
    CREATE TABLE orders (
        order_id SERIAL PRIMARY KEY,
        customer_id INT,
        product_name VARCHAR(100),
        quantity INT,
        price NUMERIC(10, 2),
        order_date DATE
    );
""")
conn.commit()

products = [
    "Laptop Pro 15",
    "Wireless Mouse",
    "Mechanical Keyboard",
    "UltraWide Monitor",
    "Noise Cancelling Headphones",
    "USB-C Hub",
    "External SSD 1TB",
    "Smartphone X",
    "Smart Watch",
    "Gaming Chair",
]

print("Generating 2000 records for PostgreSQL...")

base_date = datetime.now() - timedelta(days=365)
records = []

for i in range(1, 2001):
  customer_id = random.randint(100, 500)
  product_name = random.choice(products)
  quantity = random.randint(1, 5)
  price = round(random.uniform(50.0, 1200.0), 2)
  order_date = (base_date + timedelta(days=random.randint(0, 365))).strftime(
      "%Y-%m-%d"
  )
  records.append((customer_id, product_name, quantity, price, order_date))

cur.executemany(
    """
    INSERT INTO orders (customer_id, product_name, quantity, price, order_date)
    VALUES (%s, %s, %s, %s, %s)
""",
    records,
)

conn.commit()
cur.close()
conn.close()

print("PostgreSQL setup and seeding with 2000 records completed successfully.")