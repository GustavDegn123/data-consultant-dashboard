import pandas as pd

def sales_by_country(df):
    return df.groupby("country2")["Sales_USD"].sum().sort_values(ascending=False)

def customer_coordinates(df):
    return df.groupby("Account")[["latitude2", "longitude"]].first().dropna()
