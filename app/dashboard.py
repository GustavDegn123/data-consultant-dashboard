import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
from streamlit_folium import st_folium
from scripts.load_data import load_accounts, load_plant_hierarchy, load_sales_data
from scripts.preprocess import convert_date_column, join_data
from scripts.metrics import time_metrics as tm
from scripts.plots import time_plots as tp
from scripts.metrics import product_metrics as pm
from scripts.plots import product_plots as pp
from scripts.metrics import customer_metrics as cm
from scripts.plots import customer_plots as cp
from scripts.metrics import geo_metrics as gm
from scripts.plots import geo_plots as gp

# Sideopsætning
st.set_page_config(page_title="Salgsanalyse", layout="wide")

# Header
st.title("📊 Data Consultant Dashboard")
st.markdown("Denne rapport er baseret på virksomhedens egne salgs- og kundeoplysninger. Brug menuen i venstre side til at vælge analysen.")

# Indlæs og preprocess data
with st.spinner("Indlæser data..."):
    accounts = load_accounts()
    products = load_plant_hierarchy()
    sales = load_sales_data()
    sales = convert_date_column(sales)
    merged_df = join_data(sales, accounts, products)

# Sidebar navigation
st.sidebar.title("🔍 Vælg analyse")
option = st.sidebar.radio("Gå til:", [
    "Månedligt salg",
    "Top produkter",
    "Top kunder",
    "Tidsbaserede analyser",
    "Kundegeografi",
])

# === VISUALISERINGER === #

if option == "Tidsbaserede analyser":
    st.header("🕒 Tidsbaserede analyser")

    st.subheader("Total omsætning pr. måned")
    monthly_sales = tm.sales_over_time(merged_df, time_unit="M")
    fig1 = tp.plot_series(monthly_sales, "Månedlig omsætning", "Måned", "USD")
    st.pyplot(fig1)

    st.subheader("Antal ordrer pr. måned")
    monthly_orders = tm.order_counts_over_time(merged_df, time_unit="M")
    fig2 = tp.plot_series(monthly_orders, "Månedligt antal ordrer", "Måned", "Antal ordrer")
    st.pyplot(fig2)

    st.subheader("Gennemsnitligt antal enheder per ordre")
    avg_qty = tm.avg_quantity_per_order(merged_df)
    st.metric(label="Gennemsnitlig mængde per ordre", value=round(avg_qty, 2))

    st.subheader("Udvikling i gennemsnitlig salgspris")
    avg_price = tm.avg_price_over_time(merged_df, time_unit="M")
    fig3 = tp.plot_series(avg_price, "Gennemsnitlig salgspris (månedlig)", "Måned", "Pris i USD")
    st.pyplot(fig3)

    st.subheader("Omsætning fordelt på ugedage")
    weekday_sales = tm.sales_by_weekday(merged_df)
    fig4 = tp.plot_series(weekday_sales, "Omsætning pr. ugedag", "Ugedag", "USD")
    st.pyplot(fig4)

elif option == "Månedligt salg":
    st.header("📈 Månedligt salg")
    fig = tp.plot_series(tm.sales_over_time(merged_df, "M"), "Månedlig omsætning", "Måned", "USD")
    st.pyplot(fig)

elif option == "Top produkter":
    st.header("🏆 Produktanalyser")

    st.subheader("Top 10 bedst sælgende produkter")
    top10 = pm.top_products_total(merged_df)
    fig1 = pp.plot_bar_series(top10, "Top 10 produkter", "Produkt", "Salg i USD")
    st.pyplot(fig1)

    st.subheader("Produkter med højest profit")
    profit = pm.highest_margin_products(merged_df)
    fig2 = pp.plot_bar_series(profit, "Top 10 profitprodukter", "Produkt", "Profit i USD")
    st.pyplot(fig2)

    st.subheader("Gennemsnitlig salgspris pr. produkt")
    avg_price = pm.avg_price_per_product(merged_df).head(10)
    fig3 = pp.plot_bar_series(avg_price, "Top 10 efter salgspris", "Produkt", "Pris i USD")
    st.pyplot(fig3)

    st.subheader("Salg pr. produktstørrelse")
    size_sales = pm.sales_by_product_size(merged_df)
    fig4 = pp.plot_bar_series(size_sales, "Salg pr. størrelse", "Størrelse", "Salg i USD")
    st.pyplot(fig4)

    st.subheader("Salg pr. produktfamilie")
    fam_sales = pm.sales_by_family(merged_df).head(10)
    fig5 = pp.plot_bar_series(fam_sales, "Top 10 familier", "Familie", "Salg i USD")
    st.pyplot(fig5)

    st.subheader("Produkttrends over tid")
    trend_data = pm.product_sales_trend(merged_df)
    fig6 = pp.plot_trend(trend_data, "Produkttrends", "Måned", "Salg i USD")
    st.pyplot(fig6)

elif option == "Top kunder":
    st.header("👥 Kundeanalyser")

    st.subheader("Top 10 kunder efter omsætning")
    top_customers = cm.top_customers_by_sales(merged_df)
    fig1 = cp.plot_bar(top_customers, "Topkunder", "Kunde", "Omsætning i USD")
    st.pyplot(fig1)

    st.subheader("Loyale kunder (flere køb)")
    loyal = cm.loyal_customers(merged_df)
    st.write(f"Antal loyale kunder: {len(loyal)}")

    st.subheader("Kunder med kun ét køb")
    one_time = cm.one_time_customers(merged_df)
    st.write(f"Antal engangskunder: {len(one_time)}")

    st.subheader("Pareto-analyse (80/20)")
    pareto = cm.pareto_analysis(merged_df)
    fig2 = cp.plot_line(pareto, "Kumulativ salgsandel", "Kunde (sorteret)", "Andel af samlet omsætning")
    st.pyplot(fig2)

elif option == "Kundegeografi":
    st.header("🌍 Geografisk analyse")

    st.subheader("Salg pr. land")
    country_sales = gm.sales_by_country(merged_df)
    fig1 = gp.plot_country_sales(country_sales)
    st.pyplot(fig1)

    st.subheader("Kundelokationer (interaktivt kort)")
    coords = gm.customer_coordinates(merged_df)
    map_ = gp.plot_customer_map(coords)
    st_folium(map_, width=700)


