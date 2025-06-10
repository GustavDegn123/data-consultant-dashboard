import plotly.express as px
import pandas as pd

def plot_daily_orders(df, granularity="Dag"):
    df = df.copy()
    df["order_date"] = df["order_purchase_timestamp"]

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
    from scripts.load_olist_data import load_category_translation
    translation_df = load_category_translation()

    df = df.merge(translation_df, how="left", on="product_category_name")
    df["kategori_navn"] = df["product_category_name_danish"].fillna(df["product_category_name"])

    top_categories = (
        df.groupby("kategori_navn")["order_item_id"]
        .count()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    fig = px.bar(
        top_categories,
        x="kategori_navn",
        y="order_item_id",
        title="📦 Top 10 mest solgte produktkategorier",
        labels={"kategori_navn": "Produktkategori", "order_item_id": "Antal solgte enheder"}
    )
    fig.update_layout(xaxis_tickangle=-45)

    return fig, top_categories
