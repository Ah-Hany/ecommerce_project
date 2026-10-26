import streamlit as st
import pandas as pd
import os

# إعدادات الصفحة
st.set_page_config(page_title="E-Commerce CRM & Sales Dashboard", page_icon="📊", layout="wide")

st.title("📊 E-Commerce Sales & CRM Analytics Dashboard")
st.markdown("---")

# تحميل البيانات المجهزة
@st.cache_data
def load_data():
    if os.path.exists("final_sales_report.csv"):
        return pd.read_csv("final_sales_report.csv")
    else:
        return None

df = load_data()

if df is not None and not df.empty:
    # 1. KPIs (المؤشرات الرئيسية للأداء)
    total_revenue = df['total_revenue'].sum()
    total_orders = df['total_orders'].sum()
    total_items_sold = df['total_quantity_sold'].sum()
    avg_store_rating = df['average_rating'].mean()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("💰 Total Revenue", f"${total_revenue:,.2f}")
    col2.metric("🛒 Total Orders", f"{total_orders:,}")
    col3.metric("📦 Items Sold", f"{total_items_sold:,}")
    col4.metric("⭐ Avg Rating", f"{avg_store_rating:.2f} / 5.0")

    st.markdown("---")

    # 2. Charts & Visualizations
    col_a, col_b = st.columns(2)

    with col_a:
        st.subheader("🔥 Top Revenue by Product")
        st.bar_chart(df.set_index('product_name')['total_revenue'])

    with col_b:
        st.subheader("📦 Quantity Sold per Product")
        st.bar_chart(df.set_index('product_name')['total_quantity_sold'])

    st.markdown("---")

    # 3. Data Table
    st.subheader("📋 Detailed Product Performance Report")
    st.dataframe(df, use_container_width=True)

else:
    st.warning("⚠️ No report data found! Please run the ETL pipeline (Day 3 script) first to generate 'final_sales_report.csv'.")