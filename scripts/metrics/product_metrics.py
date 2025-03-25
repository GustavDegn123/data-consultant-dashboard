import pandas as pd

def top_products(df, time_unit="M", n=10):
    df["Date_Time"] = pd.to_datetime(df["Date_Time"], errors="coerce")
    df["period"] = df["Date_Time"].dt.to_period(time_unit)
    return df.groupby(["period", "Product_Name"])["Sales_USD"].sum().reset_index()

def top_products_total(df, n=10):
    return df.groupby("Product_Name")["Sales_USD"].sum().sort_values(ascending=False).head(n)

def highest_margin_products(df, n=10):
    df["Profit"] = df["Sales_USD"] - df["COGS_USD"]
    return df.groupby("Product_Name")["Profit"].sum().sort_values(ascending=False).head(n)

def avg_price_per_product(df):
    return df.groupby("Product_Name")["Price_USD"].mean().sort_values(ascending=False)

def product_sales_trend(df):
    df["Date_Time"] = pd.to_datetime(df["Date_Time"])
    df["Month"] = df["Date_Time"].dt.to_period("M")
    return df.groupby(["Month", "Product_Name"])["Sales_USD"].sum().reset_index()

def sales_by_product_size(df):
    return df.groupby("Product_Size")["Sales_USD"].sum().sort_values(ascending=False)

def sales_by_family(df):
    return df.groupby("Product_Family")["Sales_USD"].sum().sort_values(ascending=False)
