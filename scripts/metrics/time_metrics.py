import pandas as pd

def sales_over_time(df, time_unit="M"):
    df["Date_Time"] = pd.to_datetime(df["Date_Time"])
    grouped = df.groupby(df["Date_Time"].dt.to_period(time_unit))["Sales_USD"].sum()
    return grouped

def order_counts_over_time(df, time_unit="M"):
    df["Date_Time"] = pd.to_datetime(df["Date_Time"])
    grouped = df.groupby(df["Date_Time"].dt.to_period(time_unit))["Sales_USD"].count()
    return grouped

def avg_quantity_per_order(df):
    return df["quantity"].mean()

def avg_price_over_time(df, time_unit="M"):
    df["Date_Time"] = pd.to_datetime(df["Date_Time"])
    grouped = df.groupby(df["Date_Time"].dt.to_period(time_unit))["Price_USD"].mean()
    return grouped

def sales_by_weekday(df):
    df["Date_Time"] = pd.to_datetime(df["Date_Time"])
    df["weekday"] = df["Date_Time"].dt.day_name()
    grouped = df.groupby("weekday")["Sales_USD"].sum().reindex([
        "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"
    ])
    return grouped
