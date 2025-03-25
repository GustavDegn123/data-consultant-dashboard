import pandas as pd
import matplotlib.pyplot as plt

def plot_monthly_sales(df, date_col="Date_Time", value_col="Sales_USD"):
    df[date_col] = pd.to_datetime(df[date_col], errors="coerce")
    monthly_sales = df.groupby(df[date_col].dt.to_period("M"))[value_col].sum()

    fig, ax = plt.subplots(figsize=(10, 5))
    monthly_sales.plot(kind="bar", ax=ax)
    ax.set_title("Månedligt salg (USD)")
    ax.set_xlabel("Måned")
    ax.set_ylabel("Salg i USD")
    plt.tight_layout()
    return fig

def top_products_by_sales(df, n=5):
    top_products = df.groupby("Product_Name")["Sales_USD"].sum().sort_values(ascending=False).head(n)

    fig, ax = plt.subplots(figsize=(8, 4))
    top_products.plot(kind="bar", ax=ax)
    ax.set_title(f"Top {n} produkter efter omsætning")
    ax.set_xlabel("Produkt")
    ax.set_ylabel("Omsætning i USD")
    plt.tight_layout()
    return fig

def top_customers(df, n=5):
    top_accounts = df.groupby("Account")["Sales_USD"].sum().sort_values(ascending=False).head(n)

    fig, ax = plt.subplots(figsize=(8, 4))
    top_accounts.plot(kind="bar", ax=ax)
    ax.set_title(f"Top {n} kunder efter samlet køb")
    ax.set_xlabel("Kunde")
    ax.set_ylabel("Salg i USD")
    plt.tight_layout()
    return fig

def sales_by_country(df):
    country_sales = df.groupby("country2")["Sales_USD"].sum().sort_values(ascending=False)

    fig, ax = plt.subplots(figsize=(10, 5))
    country_sales.plot(kind="bar", ax=ax)
    ax.set_title("Salg fordelt på lande")
    ax.set_xlabel("Land")
    ax.set_ylabel("Salg i USD")
    plt.tight_layout()
    return fig

def avg_price_and_cost(df):
    avg_df = df.groupby("Product_Name")[["Price_USD", "COGS_USD"]].mean().sort_values("Price_USD", ascending=False).head(10)

    fig, ax = plt.subplots(figsize=(10, 5))
    avg_df.plot(kind="bar", ax=ax)
    ax.set_title("Gennemsnitlig salgspris og COGS (Top 10 produkter)")
    ax.set_ylabel("USD")
    plt.tight_layout()
    return fig

def product_profit_margin(df, n=5):
    df["Profit"] = df["Sales_USD"] - df["COGS_USD"]
    profit_df = df.groupby("Product_Name")["Profit"].sum().sort_values(ascending=False).head(n)

    fig, ax = plt.subplots(figsize=(8, 4))
    profit_df.plot(kind="bar", ax=ax)
    ax.set_title(f"Top {n} produkter efter samlet profit")
    ax.set_ylabel("Profit (USD)")
    plt.tight_layout()
    return fig

def top_product_families(df, n=5):
    top_families = df.groupby("Product_Family")["Sales_USD"].sum().sort_values(ascending=False).head(n)

    fig, ax = plt.subplots(figsize=(8, 4))
    top_families.plot(kind="bar", ax=ax)
    ax.set_title(f"Top {n} produktfamilier efter omsætning")
    ax.set_ylabel("Salg i USD")
    plt.tight_layout()
    return fig
