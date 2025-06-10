import pandas as pd

def compute_delivery_time_by_month(df_orders):
    df = df_orders.copy()
    df["order_purchase_timestamp"] = pd.to_datetime(df["order_purchase_timestamp"])
    df["order_delivered_customer_date"] = pd.to_datetime(df["order_delivered_customer_date"])
    
    df["delivery_time_days"] = (df["order_delivered_customer_date"] - df["order_purchase_timestamp"]).dt.days
    df["month"] = df["order_purchase_timestamp"].dt.to_period("M").astype(str)

    result = df.groupby("month")["delivery_time_days"].mean().reset_index()
    return result

def prepare_geo_data(customers, sellers, geo):
    # Fjern dubletter i geolocation-data
    geo_clean = geo.drop_duplicates(subset=["geolocation_zip_code_prefix"])
    
    # Merge med customers
    customers_geo = customers.merge(
        geo_clean, left_on="customer_zip_code_prefix", right_on="geolocation_zip_code_prefix", how="left"
    )
    customers_geo["type"] = "Kunde"

    # Merge med sellers
    sellers_geo = sellers.merge(
        geo_clean, left_on="seller_zip_code_prefix", right_on="geolocation_zip_code_prefix", how="left"
    )
    sellers_geo["type"] = "Sælger"

    # Vælg relevante kolonner og saml
    combined = pd.concat([
        customers_geo[["geolocation_lat", "geolocation_lng", "type"]],
        sellers_geo[["geolocation_lat", "geolocation_lng", "type"]]
    ])

    return combined.dropna()
