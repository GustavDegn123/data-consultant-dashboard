# scripts/load_olist_data.py
import pandas as pd
import os

DATA_DIR = "data/olist"

def load_orders():
    return pd.read_csv(os.path.join(DATA_DIR, "olist_orders_dataset.csv"))

def load_order_items():
    return pd.read_csv(os.path.join(DATA_DIR, "olist_order_items_dataset.csv"))

def load_products():
    return pd.read_csv(os.path.join(DATA_DIR, "olist_products_dataset.csv"))

def load_category_translation():
    return pd.read_csv(os.path.join(DATA_DIR, "product_category_name_translation.csv"))

def load_customers():
    return pd.read_csv(os.path.join(DATA_DIR, "olist_customers_dataset.csv"))

def load_sellers():
    return pd.read_csv(os.path.join(DATA_DIR, "olist_sellers_dataset.csv"))

def load_geolocation():
    return pd.read_csv(os.path.join(DATA_DIR, "olist_geolocation_dataset.csv"))

def load_order_reviews():
    return pd.read_csv(os.path.join(DATA_DIR, "olist_order_reviews_dataset.csv"))

def load_order_payments():
    return pd.read_csv(os.path.join(DATA_DIR, "olist_order_payments_dataset.csv"))

def get_sales_data():
    orders = load_orders()
    items = load_order_items()
    products = load_products()
    payments = load_order_payments()  # ← tilføj denne linje
    categories = load_category_translation()
    categories_da = pd.read_csv(os.path.join(DATA_DIR, "category_translation_da.csv"))

    products = products.merge(categories, on="product_category_name", how="left")
    products = products.merge(categories_da, on="product_category_name_english", how="left")

    merged = orders.merge(items, on="order_id", how="left") \
                   .merge(products, on="product_id", how="left") \
                   .merge(payments, on="order_id", how="left")  # ← tilføj denne merge
    return merged
