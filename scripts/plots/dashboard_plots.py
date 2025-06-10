import plotly.express as px
import pandas as pd

def plot_daily_orders(df, granularity="Dag"):
    # Omdøb kolonne til konsistent navn
    df = df.copy()
    df["order_date"] = df["order_purchase_timestamp"]

    # Konverter efter valgt granularitet
    if granularity == "Dag":
        df["date"] = df["order_date"].dt.date
    elif granularity == "Måned":
        df["date"] = df["order_date"].dt.to_period("M").dt.to_timestamp()
    elif granularity == "År":
        df["date"] = df["order_date"].dt.to_period("Y").dt.to_timestamp()

    orders_by_date = df.groupby("date").size().reset_index(name="orders")

    fig = px.line(orders_by_date, x="date", y="orders", title=f"{granularity}-vise ordrer")
    fig.update_layout(xaxis_title="Dato", yaxis_title="Antal ordrer")
    return fig

def plot_payment_distribution(payment_df):
    return px.pie(payment_df, names="payment_type", title="💳 Fordeling af betalingstyper")

def plot_top_categories(df):
    top_products = (
        df.groupby("product_category_name")["order_item_id"]
        .count()
        .sort_values(ascending=False)
        .head(5)
        .reset_index()
    )
    return top_products.rename(columns={"product_category_name": "Kategori", "order_item_id": "Solgte enheder"})
