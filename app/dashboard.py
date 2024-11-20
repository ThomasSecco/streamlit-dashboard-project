import streamlit as st
import pandas as pd
import altair as alt

# Load Data
@st.cache
def load_data():
    data = pd.read_csv('data/global_superstore.csv', encoding='latin1' , parse_dates=['Order Date'])
    return data

data = load_data()

# Dashboard Title
st.title("Global Superstore Dashboard")
st.markdown("Explore sales and profit trends across categories and regions.")

# Sidebar Filters
st.sidebar.header("Filters")
category_filter = st.sidebar.multiselect(
    "Select Categories", options=data['Category'].unique(), default=data['Category'].unique()
)
region_filter = st.sidebar.multiselect(
    "Select Regions", options=data['Region'].unique(), default=data['Region'].unique()
)

# Apply Filters
filtered_data = data[
    (data['Category'].isin(category_filter)) & (data['Region'].isin(region_filter))
]

# Display Filtered Data
st.header("Filtered Data")
st.write(filtered_data)

# Visualizations
st.header("Visualizations")

# Sales Trend Line Chart
st.subheader("Sales Trend Over Time")
sales_trend = alt.Chart(filtered_data).mark_line().encode(
    x='Order Date:T',
    y='Sales:Q',
    color='Region:N',
    tooltip=['Order Date', 'Sales', 'Region']
).interactive()
st.altair_chart(sales_trend, use_container_width=True)

# Profit by Category Bar Chart
st.subheader("Profit by Category")
profit_category = alt.Chart(filtered_data).mark_bar().encode(
    x='Category:N',
    y='Profit:Q',
    color='Category:N',
    tooltip=['Category', 'Profit']
).interactive()
st.altair_chart(profit_category, use_container_width=True)

# Sales by Sub-Category Pie Chart
st.subheader("Sales by Sub-Category")
sub_category_sales = filtered_data.groupby('Sub-Category')['Sales'].sum().reset_index()
sub_category_pie = alt.Chart(sub_category_sales).mark_arc().encode(
    theta=alt.Theta(field='Sales', type='quantitative'),
    color=alt.Color(field='Sub-Category', type='nominal'),
    tooltip=['Sub-Category', 'Sales']
)
st.altair_chart(sub_category_pie, use_container_width=True)

# Metrics
st.header("Key Metrics")
total_sales = filtered_data['Sales'].sum()
total_profit = filtered_data['Profit'].sum()
avg_profit_margin = (total_profit / total_sales) * 100

st.metric("Total Sales", f"${total_sales:,.2f}")
st.metric("Total Profit", f"${total_profit:,.2f}")
st.metric("Average Profit Margin", f"{avg_profit_margin:.2f}%")
