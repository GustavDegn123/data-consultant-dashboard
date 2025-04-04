# analysis.py
import pandas as pd
import plotly.express as px
import plotly.io as pio

def plot_monthly_sales(df, date_col="Date_Time", value_col="Sales_USD", save_path=None):
    df[date_col] = pd.to_datetime(df[date_col], errors="coerce")
    monthly_sales = df.groupby(df[date_col].dt.to_period("M"))[value_col].sum().reset_index()

    # Konverter Period til string
    if pd.api.types.is_period_dtype(monthly_sales[date_col]):
        monthly_sales[date_col] = monthly_sales[date_col].astype(str)

    fig = px.bar(monthly_sales, x=date_col, y=value_col, title="Månedligt salg (USD)")
    fig.update_layout(template="plotly_white", xaxis_title="Måned", yaxis_title="Salg i USD")

    if save_path:
        pio.write_image(fig, save_path, width=1000, height=600)

    return fig

def top_products_by_sales(df, n=5, save_path=None):
    top_products = df.groupby("Product_Name")["Sales_USD"].sum().sort_values(ascending=False).head(n).reset_index()

    fig = px.bar(top_products, x="Product_Name", y="Sales_USD", title=f"Top {n} produkter efter omsætning")
    fig.update_layout(template="plotly_white", xaxis_title="Produkt", yaxis_title="Omsætning i USD")

    if save_path:
        pio.write_image(fig, save_path, width=900, height=500)

    return fig

def top_customers(df, n=5, save_path=None):
    top_accounts = df.groupby("Account")["Sales_USD"].sum().sort_values(ascending=False).head(n).reset_index()

    fig = px.bar(top_accounts, x="Account", y="Sales_USD", title=f"Top {n} kunder efter samlet køb")
    fig.update_layout(template="plotly_white", xaxis_title="Kunde", yaxis_title="Salg i USD")

    if save_path:
        pio.write_image(fig, save_path, width=900, height=500)

    return fig

def sales_by_country(df, save_path=None):
    country_sales = df.groupby("country2")["Sales_USD"].sum().sort_values(ascending=False).reset_index()

    fig = px.bar(country_sales, x="country2", y="Sales_USD", title="Salg fordelt på lande")
    fig.update_layout(template="plotly_white", xaxis_title="Land", yaxis_title="Salg i USD")

    if save_path:
        pio.write_image(fig, save_path, width=1000, height=500)

    return fig

def avg_price_and_cost(df, save_path=None):
    avg_df = df.groupby("Product_Name")[["Price_USD", "COGS_USD"]].mean().sort_values("Price_USD", ascending=False).head(10).reset_index()

    fig = px.bar(avg_df, x="Product_Name", y=["Price_USD", "COGS_USD"], barmode="group",
                 title="Gennemsnitlig salgspris og COGS (Top 10 produkter)")
    fig.update_layout(template="plotly_white", yaxis_title="USD", xaxis_title="Produkt")

    if save_path:
        pio.write_image(fig, save_path, width=1000, height=500)

    return fig

def product_profit_margin(df, n=5, save_path=None):
    df["Profit"] = df["Sales_USD"] - df["COGS_USD"]
    profit_df = df.groupby("Product_Name")["Profit"].sum().sort_values(ascending=False).head(n).reset_index()

    fig = px.bar(profit_df, x="Product_Name", y="Profit", title=f"Top {n} produkter efter samlet profit")
    fig.update_layout(template="plotly_white", yaxis_title="Profit (USD)", xaxis_title="Produkt")

    if save_path:
        pio.write_image(fig, save_path, width=900, height=500)

    return fig

def top_product_families(df, n=5, save_path=None):
    top_families = df.groupby("Product_Family")["Sales_USD"].sum().sort_values(ascending=False).head(n).reset_index()

    fig = px.bar(top_families, x="Product_Family", y="Sales_USD", title=f"Top {n} produktfamilier efter omsætning")
    fig.update_layout(template="plotly_white", yaxis_title="Salg i USD", xaxis_title="Familie")

    if save_path:
        pio.write_image(fig, save_path, width=900, height=500)

    return fig
