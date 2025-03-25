import pandas as pd

def top_customers_by_sales(df, n=10):
    return df.groupby("Account")["Sales_USD"].sum().sort_values(ascending=False).head(n)

def loyal_customers(df):
    return df["Account"].value_counts().loc[lambda x: x > 1]

def one_time_customers(df):
    return df["Account"].value_counts().loc[lambda x: x == 1]

def pareto_analysis(df):
    sales_by_customer = df.groupby("Account")["Sales_USD"].sum().sort_values(ascending=False)
    cumulative_share = sales_by_customer.cumsum() / sales_by_customer.sum()
    return cumulative_share
