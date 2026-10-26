# End-to-End E-Commerce Data Engineering & Analytics Pipeline

An enterprise-grade, multi-source ETL pipeline and interactive analytics dashboard built with Python, PostgreSQL, MongoDB, and Streamlit.

## Project Overview
This project simulates a real-world e-commerce data pipeline:
- **Extract**: Gathers transactional order data from **PostgreSQL** and customer reviews/ratings from **MongoDB**.
- **Transform**: Cleans, standardizes data types, handles case-sensitivity, and aggregates KPIs using **Pandas**.
- **Load**: Exports processed datasets into local CSV reports and updates a relational summary schema back into **PostgreSQL**.
- **Visualize**: Powers a real-time analytics web dashboard using **Streamlit**.

## Tech Stack
- **Languages**: Python
- **Databases**: PostgreSQL, MongoDB
- **Data Processing**: Pandas, Psycopg2, PyMongo
- **Visualization**: Streamlit
- **DevOps/Logging**: Built-in Python Logging, Git/GitHub

---

## Features & Dashboards

### 1. Executive Summary & Core Metrics
- Automated data quality standardization (`str.title()`, `str.strip()`).
- High-level KPIs tracking total revenue, total orders, and overall items sold dynamically.

![Dashboard 1](images/Screenshot%202026-10-26%20201215.png)

---

### 2. Product Revenue & Customer Sentiment Insights
- Revenue and sales volume tracking broken down by product category.
- Customer sentiment integration incorporating average ratings mapped seamlessly from NoSQL reviews.

![Dashboard 2](images/Screenshot%202026-10-26%20201243.png)
