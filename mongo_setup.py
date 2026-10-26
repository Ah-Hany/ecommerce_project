from datetime import datetime, timedelta
import random
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["ecommerce_nosql"]

db.reviews.drop()
db.user_activity.drop()

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

comments_pool = [
    "Excellent product, highly recommended",
    "Acceptable quality for the price",
    "Fast shipping and original product received",
    "Poor quality, would not buy again",
    "Very good and practical",
    "Good, but shipping took too long",
    "Amazing and excellent customer service",
    "Not as expected, but does the job",
]

actions_pool = ["click_product", "add_to_cart", "purchase", "view_details", "search"]

print("Generating 2000 realistic records for MongoDB...")

reviews_list = []
base_date = datetime.now() - timedelta(days=365)

for i in range(1, 2001):
  review = {
      "review_id": i,
      "product_name": random.choice(products),
      "user_id": random.randint(100, 500),
      "rating": random.choices(
          [5, 4, 3, 2, 1], weights=[45, 30, 15, 7, 3]
      )[0],
      "comment": random.choice(comments_pool),
      "date": (
          base_date + timedelta(days=random.randint(0, 365))
      ).strftime("%Y-%m-%d"),
  }
  reviews_list.append(review)

activity_list = []
for i in range(1, 2001):
  activity = {
      "activity_id": i,
      "user_id": random.randint(100, 500),
      "action": random.choice(actions_pool),
      "target_item": random.choice(products),
      "timestamp": (
          base_date + timedelta(seconds=random.randint(0, 31536000))
      ).strftime("%Y-%m-%d %H:%M:%S"),
  }
  activity_list.append(activity)

db.reviews.insert_many(reviews_list)
db.user_activity.insert_many(activity_list)

print(
    "Successfully inserted 2000 reviews and 2000 user activities into MongoDB."
)
print("MongoDB setup and seeding completed successfully.")