import streamlit as st
import pandas as pd

# Sæt layout og sideopsætning
st.set_page_config(page_title="Knitter's Delight Dashboard", layout="wide")

# --- CSS styling ---
st.markdown("""
    <style>
    .stApp {
        background-color: #f5f5f5;
    }
    div[data-testid="stMetric"] {
        background-color: white;
        border-radius: 16px;
        padding: 20px;
        margin: 10px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }   
    div[data-testid="stMetric"]:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
    }
    .block-container h1, .block-container h2, .block-container h3 {
        margin-top: 1rem;
    }
    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 1.5rem;
    }
    .element-container:has(div.plotly-graph-div) {
        padding: 10px;
        background-color: white;
        border-radius: 16px;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
        margin: 10px 0;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .element-container:has(div.plotly-graph-div):hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
    }
    /* Add styling for dataframes to match other visualizations */
    .element-container:has(div[data-testid="dataframe"]) {
        padding: 10px;
        background-color: white;
        border-radius: 16px;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
        margin: 10px 0;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .element-container:has(div[data-testid="dataframe"]):hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
    }
    </style>
""", unsafe_allow_html=True)


# --- Importér egne moduler ---
from scripts.load_olist_data import (
    get_sales_data,
    load_customers,
    load_sellers,
    load_geolocation,
    load_order_payments,
    load_order_reviews
)

# Produkter
from scripts.metrics.product_metrics import avg_price_freight_per_category
from scripts.plots.product_plots import top_product_categories, plot_avg_price_freight

# Logistik
from scripts.metrics.logistics_metrics import compute_delivery_time_by_month, prepare_geo_data
from scripts.plots.logistics_plots import plot_delivery_time_by_month, plot_geo_map

# Betalinger
from scripts.metrics.payment_metrics import compute_payment_sums, compute_avg_installments
from scripts.plots.payment_plots import plot_payment_sums, plot_avg_installments

# Lager
from scripts.metrics.inventory_metrics import compute_weight_volume
from scripts.plots.inventory_plots import plot_weight_vs_volume

# Dashboard - nye moduler
from scripts.metrics.dashboard_metrics import compute_dashboard_kpis
from scripts.plots.dashboard_plots import plot_daily_orders, plot_payment_distribution

page = st.sidebar.radio(
    "Vælg analyseområde",
    [
        "\U0001F4CA Dashboard",         # 📊
        "\U0001F6D2 Salg & Produkter",  # 🛒
        "\U0001F69B Logistik",          # 🚛
        "\U0001F4B0 Betalinger",        # 💰
        "\U0001F4E6 Lager",             # 📦
        "\U0001F31F Kundetilfredshed"   # 🌟
    ]
)

# --- Sidebar: Dato- og granularitetsfiltrering ---
st.sidebar.markdown("---")
st.sidebar.markdown("### Filtrér data")
df_raw = get_sales_data()
df_raw["order_purchase_timestamp"] = pd.to_datetime(df_raw["order_purchase_timestamp"])

min_date = df_raw["order_purchase_timestamp"].min().date()
max_date = df_raw["order_purchase_timestamp"].max().date()

import datetime

# Quick range-valg
range_options = {
    "Egen periode": None,
    "1 dag": 1,
    "7 dage": 7,
    "30 dage": 30,
    "3 måneder": 90,
    "6 måneder": 180,
    "1 år": 365
}

range_choice = st.sidebar.selectbox("Vælg datointerval", list(range_options.keys()))
today = max_date

if range_options[range_choice] is None:
    start_date = st.sidebar.date_input("Fra", min_date)
    end_date = st.sidebar.date_input("Til", max_date)
else:
    delta_days = range_options[range_choice]
    start_date = today - datetime.timedelta(days=delta_days)
    end_date = today
    st.sidebar.markdown(f"**Periode:** {start_date} → {end_date}")

# Flyt dette udenfor if/else
granularity = st.sidebar.radio(
    "Vælg granularitet",
    ["Dag", "Måned", "År"],
    index=1  # f.eks. standard = Måned
)

# Vis som tekst i sidebar
st.sidebar.markdown(f"**Granularitet valgt:** {granularity}")

# --- Filtrer data ---
df = df_raw[(df_raw["order_purchase_timestamp"].dt.date >= start_date) &
            (df_raw["order_purchase_timestamp"].dt.date <= end_date)]

# --- Eksterne datakilder ---
delivery_df = compute_delivery_time_by_month(df)
customers = load_customers()
filtered_customer_ids = df["customer_id"].unique()
customers = customers[customers["customer_id"].isin(filtered_customer_ids)]
sellers = load_sellers()
filtered_seller_ids = df["seller_id"].unique()
sellers = sellers[sellers["seller_id"].isin(filtered_seller_ids)]
payment_df = load_order_payments()
payment_df = payment_df[payment_df["order_id"].isin(df["order_id"])]
review_df = load_order_reviews()
review_df = review_df[review_df["order_id"].isin(df["order_id"])]
geo = load_geolocation()[["geolocation_zip_code_prefix", "geolocation_lat", "geolocation_lng"]]

if page == "📊 Dashboard":
    st.title("📊 Overblik – Knitter's Delight")

    kpis = compute_dashboard_kpis(df, delivery_df, customers, sellers, review_df)

    # Visuelle KPI-kort
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("📦 Antal ordrer", f"{kpis['num_orders']:,}")
    col2.metric("🚒 Solgte produkter", f"{kpis['num_products']:,}")
    col3.metric("💰 Total omsætning", f"{kpis['total_revenue']:,.0f} DKK")
    col4.metric("🌟 Gennemsnitlig review-score", f"{kpis['avg_review']:.2f}")

    col5, col6, col7, col8 = st.columns(4)
    col5.metric("🚚 Gennemsnitlig leveringstid", f"{kpis['avg_delivery']:.1f} dage")
    col6.metric("📦 Gennemsnitlig fragtomkostning", f"{kpis['avg_freight']:.2f} DKK")
    col7.metric("👥 Antal kunder", f"{kpis['num_customers']:,}")
    col8.metric("🏬 Antal sælgere", f"{kpis['num_sellers']:,}")

    # Sektion: Ordrer og betalinger
    st.markdown("### 📅 Ordrer og betalinger")
    col9, col10 = st.columns(2)
    with col9:
        st.plotly_chart(plot_daily_orders(df, granularity), use_container_width=True)
    with col10:
        st.plotly_chart(plot_payment_distribution(payment_df), use_container_width=True)

    # Sektion: Kort og topkategorier
    st.markdown("### 🗺️ Kort og topkategorier")
    geo_df = prepare_geo_data(customers, sellers, geo)
    geo_fig = plot_geo_map(geo_df)

    col11, col12 = st.columns([2, 1])
    with col11:
        st.plotly_chart(geo_fig, use_container_width=True)
    with col12:
        from scripts.plots.dashboard_plots import plot_top_categories
        fig, top_df = plot_top_categories(df)
        st.plotly_chart(fig, use_container_width=True)

# --- Side 1: Salg & Produkter ---
if page == "🛒 Salg & Produkter":
    st.title("🛒 Salg og Produktanalyse")

    st.subheader("Top 10 mest solgte produktkategorier")
    fig1 = top_product_categories(df)
    st.plotly_chart(fig1)

    st.subheader("Gennemsnitspris og fragt pr. produktkategori")
    avg_df = avg_price_freight_per_category(df)
    fig2 = plot_avg_price_freight(avg_df)
    st.plotly_chart(fig2)

# --- Side 2: Logistik ---
elif page == "🚛 Logistik":
    st.title("🚛 Logistikanalyse")

    st.subheader("📦 Gennemsnitlig leveringstid pr. måned")
    delivery_df = compute_delivery_time_by_month(df)
    fig = plot_delivery_time_by_month(delivery_df)
    st.plotly_chart(fig)

    st.subheader("🗺️ Kort over kunder og sælgere")
    customers = load_customers()[["customer_id", "customer_zip_code_prefix"]].drop_duplicates()
    sellers = load_sellers()[["seller_id", "seller_zip_code_prefix"]].drop_duplicates()
    geo = load_geolocation()[["geolocation_zip_code_prefix", "geolocation_lat", "geolocation_lng"]]

    geo_df = prepare_geo_data(customers, sellers, geo)
    geo_fig = plot_geo_map(geo_df)
    st.plotly_chart(geo_fig)

# --- Side 3: Betalinger ---
elif page == "💰 Betalinger":
    st.title("💰 Betalingsanalyse")

    payment_df = load_order_payments()

    st.subheader("Fordeling af betalingstyper")
    sums_df = compute_payment_sums(payment_df)
    fig1 = plot_payment_sums(sums_df)
    st.plotly_chart(fig1)

    st.subheader("Antal afbetalinger pr. betalingstype")
    avg_inst_df = compute_avg_installments(payment_df)
    fig2 = plot_avg_installments(avg_inst_df)
    st.plotly_chart(fig2)

# --- Side 4: Lager ---
elif page == "📦 Lager":
    st.title("📦 Lageranalyse")

    st.subheader("Volumen og vægt af produkter")
    weight_volume_df = compute_weight_volume(df)
    fig = plot_weight_vs_volume(weight_volume_df)
    st.plotly_chart(fig)

# --- Side 5: Kundetilfredshed ---
elif page == "🌟 Kundetilfredshed":
    st.title("🌟 Kundetilfredshedsanalyse")

    from scripts.load_olist_data import load_order_reviews
    from scripts.metrics.review_metrics import compute_review_score_distribution, compute_reviews_per_category
    from scripts.plots.review_plots import plot_review_score_distribution, plot_reviews_per_category

    review_df = load_order_reviews()

    st.subheader("Fordeling af anmeldelsesscore")
    dist_df = compute_review_score_distribution(review_df)
    fig1 = plot_review_score_distribution(dist_df)
    st.plotly_chart(fig1)

    st.subheader("Gennemsnitlig anmeldelsesscore pr. produktkategori")
    # Husk at genindlæse nødvendige datakilder
    from scripts.load_olist_data import load_order_items, load_products, load_category_translation

    order_items = load_order_items()
    products = load_products()
    categories = load_category_translation()

    review_cat_df = compute_reviews_per_category(review_df, order_items, products, categories)
    fig2 = plot_reviews_per_category(review_cat_df)
    st.plotly_chart(fig2)