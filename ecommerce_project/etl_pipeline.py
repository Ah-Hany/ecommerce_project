import logging
import psycopg2
from pymongo import MongoClient
import pandas as pd

# إعداد الـ Logging
logging.basicConfig(
    filename='etl_process.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logging.info("Starting E-commerce ETL Pipeline - Day 5 (Production Ready)")

# ==========================================
# 1. EXTRACT PHASE
# ==========================================
try:
    pg_conn = psycopg2.connect(
        dbname="ecommerce_source",
        user="postgres",
        password="42024137",
        host="localhost",
        port="5432"
    )
    pg_cur = pg_conn.cursor()
    pg_cur.execute("SELECT customer_id, product_name, quantity, price, order_date FROM orders;")
    pg_orders = pg_cur.fetchall()
    logging.info(f"Successfully extracted {len(pg_orders)} orders from PostgreSQL.")
except Exception as e:
    logging.error(f"Error connecting to PostgreSQL: {e}")
    pg_orders = []

try:
    mongo_client = MongoClient("mongodb://localhost:27017/")
    mongo_db = mongo_client["ecommerce_nosql"]
    mongo_reviews = list(mongo_db["reviews"].find({}, {"_id": 0}))
    logging.info(f"Successfully extracted {len(mongo_reviews)} reviews from MongoDB.")
except Exception as e:
    logging.error(f"Error connecting to MongoDB: {e}")
    mongo_reviews = []

# ==========================================
# 2. TRANSFORM PHASE
# ==========================================
orders_df = pd.DataFrame(pg_orders, columns=['customer_id', 'product_name', 'quantity', 'price', 'order_date'])
orders_df['total_sales'] = orders_df['quantity'] * orders_df['price']
orders_df['clean_product_name'] = orders_df['product_name'].astype(str).str.strip().str.title()

reviews_df = pd.DataFrame(mongo_reviews)

if not reviews_df.empty and 'product_name' in reviews_df.columns and 'rating' in reviews_df.columns:
    reviews_df['clean_product_name'] = reviews_df['product_name'].astype(str).str.strip().str.title()
    product_ratings = reviews_df.groupby('clean_product_name')['rating'].mean().reset_index()
    product_ratings.rename(columns={'rating': 'average_rating'}, inplace=True)
else:
    product_ratings = pd.DataFrame(columns=['clean_product_name', 'average_rating'])

product_sales_summary = orders_df.groupby('clean_product_name').agg(
    total_orders=('customer_id', 'count'),
    total_revenue=('total_sales', 'sum'),
    total_quantity_sold=('quantity', 'sum')
).reset_index()

final_report_df = pd.merge(product_sales_summary, product_ratings, on='clean_product_name', how='left')
final_report_df['average_rating'] = final_report_df['average_rating'].fillna(0.0).round(2)
final_report_df['total_revenue'] = final_report_df['total_revenue'].round(2)
final_report_df.rename(columns={'clean_product_name': 'product_name'}, inplace=True)

logging.info("Data successfully cleaned, standardized, and merged.")

# ==========================================
# 3. LOAD PHASE
# ==========================================
csv_filename = "final_sales_report.csv"
final_report_df.to_csv(csv_filename, index=False)
logging.info(f"Saved report locally to '{csv_filename}'")

try:
    pg_cur.execute("""
        CREATE TABLE IF NOT EXISTS sales_summary (
            product_name VARCHAR(100) PRIMARY KEY,
            total_orders INT,
            total_revenue NUMERIC(12, 2),
            total_quantity_sold INT,
            average_rating NUMERIC(3, 2)
        );
    """)

    for _, row in final_report_df.iterrows():
        pg_cur.execute("""
            INSERT INTO sales_summary (product_name, total_orders, total_revenue, total_quantity_sold, average_rating)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (product_name) 
            DO UPDATE SET 
                total_orders = EXCLUDED.total_orders,
                total_revenue = EXCLUDED.total_revenue,
                total_quantity_sold = EXCLUDED.total_quantity_sold,
                average_rating = EXCLUDED.average_rating;
        """, (
            row['product_name'], int(row['total_orders']), float(row['total_revenue']),
            int(row['total_quantity_sold'], ),
            float(row['average_rating'])))

    pg_conn.commit()
    logging.info("Successfully loaded summary data into PostgreSQL table 'sales_summary'.")
except Exception as e:
    logging.error(f"Error loading data into PostgreSQL: {e}")

if 'pg_cur' in locals(): pg_cur.close()
if 'pg_conn' in locals(): pg_conn.close()
if 'mongo_client' in locals(): mongo_client.close()

logging.info("ETL Pipeline Day 5 execution completed successfully.")
