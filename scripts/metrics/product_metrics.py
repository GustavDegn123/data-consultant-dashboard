# scripts/metrics/product_metrics.py
def avg_price_freight_per_category(df):
    df = df.dropna(subset=["product_category_name_danish"])
    grouped = df.groupby("product_category_name_danish")[["price", "freight_value"]].mean().reset_index()
    return grouped
