def compute_dashboard_kpis(df, delivery_df, customers_df, sellers_df, review_df):
    return {
        "num_orders": df["order_id"].nunique(),
        "num_products": df["product_id"].nunique(),
        "total_revenue": df["payment_value"].sum(),
        "avg_review": review_df["review_score"].mean(),
        "avg_freight": df["freight_value"].mean(),
        "avg_delivery": delivery_df["delivery_time_days"].mean(),
        "num_customers": customers_df["customer_id"].nunique(),
        "num_sellers": sellers_df["seller_id"].nunique(),
    }
