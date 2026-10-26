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

## Features & Dashboards

- Automated data quality standardization (`str.title()`, `str.strip()`).
- Revenue and sales volume tracking by product category.
- Customer sentiment integration (Average ratings mapped from NoSQL reviews).

### 1. Dashboard Overview & Metrics
![Dashboard 1](Screenshot%202026-10-26-173322.png)

### 2. Analytics & Detailed Insights
![Dashboard 2](Screenshot%202026-10-26-173354.png)
