import streamlit as st
from scripts.load_olist_data import get_sales_data
from scripts.plots.product_plots import top_product_categories

st.title("📊 Knitter’s Delight – Produktanalyse")

# Indlæs data
df = get_sales_data()

# Visualisering: Top produktkategorier
st.subheader("Top 10 mest solgte produktkategorier")
fig = top_product_categories(df)
st.plotly_chart(fig)
