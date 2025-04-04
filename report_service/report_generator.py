import os
from fpdf import FPDF
from datetime import datetime
from report_service.mailer import send_email
from report_service.customer_manager import get_customer_info
from scripts.load_data import load_accounts, load_plant_hierarchy, load_sales_data
from scripts.preprocess import convert_date_column, join_data
from scripts.analysis import (
    plot_monthly_sales,
    top_products_by_sales,
    top_customers,
    sales_by_country,
    avg_price_and_cost,
    product_profit_margin,
    top_product_families
)
from scripts.metrics import time_metrics as tm
from scripts.metrics import product_metrics as pm
from scripts.metrics import customer_metrics as cm
from scripts.metrics import geo_metrics as gm
from scripts.plots import time_plots as tp
from scripts.plots import customer_plots as cp
from scripts.plots import product_plots as pp
from scripts.plots import geo_plots as gp

REPORT_DIR = "generated_reports"
os.makedirs(REPORT_DIR, exist_ok=True)

def generate_figures(df, prefix):
    image_paths = []

    def save(fig_func, *args, suffix, **kwargs):
        path = os.path.join(REPORT_DIR, f"{prefix}_{suffix}.png")
        fig_func(*args, save_path=path, **kwargs)
        image_paths.append(path)

    # ANALYSIS.PY
    save(plot_monthly_sales, df, suffix="monthly_sales")
    save(top_products_by_sales, df, suffix="top_products")
    save(top_customers, df, suffix="top_customers")
    save(sales_by_country, df, suffix="sales_by_country")
    save(avg_price_and_cost, df, suffix="avg_price_cost")
    save(product_profit_margin, df, suffix="profit_products")
    save(top_product_families, df, suffix="top_families")

    # TIME PLOTS
    monthly_sales = tm.sales_over_time(df, "M")
    save(tp.plot_series, monthly_sales, "Månedlig omsætning", "Måned", "USD", suffix="time_monthly_sales")

    monthly_orders = tm.order_counts_over_time(df, "M")
    save(tp.plot_series, monthly_orders, "Ordrer pr. måned", "Måned", "Antal ordrer", suffix="time_orders")

    avg_price = tm.avg_price_over_time(df, "M")
    save(tp.plot_series, avg_price, "Gns. pris over tid", "Måned", "USD", suffix="avg_price_over_time")

    weekday_sales = tm.sales_by_weekday(df)
    save(tp.plot_series, weekday_sales, "Omsætning pr. ugedag", "Ugedag", "USD", suffix="weekday_sales")

    # PRODUCT PLOTS
    size_sales = pm.sales_by_product_size(df)
    save(pp.plot_bar_series, size_sales, "Salg pr. størrelse", "Størrelse", "USD", suffix="product_size_sales")

    fam_sales = pm.sales_by_family(df).head(10)
    save(pp.plot_bar_series, fam_sales, "Top familier", "Familie", "USD", suffix="product_families")

    trend_data = pm.product_sales_trend(df)
    save(pp.plot_trend, trend_data, "Produkttrends", "Måned", "Salg i USD", suffix="product_trends")

    # CUSTOMER PLOTS
    top_cust = cm.top_customers_by_sales(df)
    save(cp.plot_bar, top_cust, "Top kunder", "Kunde", "USD", suffix="top_customers_by_sales")

    pareto = cm.pareto_analysis(df)
    save(cp.plot_line, pareto, "Pareto (80/20)", "Kunde (sorteret)", "Andel", suffix="pareto")

    # GEO PLOTS
    country_sales = gm.sales_by_country(df)
    save(gp.plot_country_sales, country_sales, suffix="geo_sales_by_country")

    return image_paths

def generate_pdf_report(customer_id):
    customer = get_customer_info(customer_id)
    if not customer:
        raise ValueError(f"Kunde med id '{customer_id}' findes ikke.")

    name = customer["name"]
    email = customer["email"]

    # Load og merge data
    accounts = load_accounts()
    products = load_plant_hierarchy()
    sales = load_sales_data()
    sales = convert_date_column(sales)
    merged_df = join_data(sales, accounts, products)

    # Generer figurer og få stier
    image_paths = generate_figures(merged_df, prefix=customer_id)

    # Tekstbeskrivelser pr. figur
    descriptions = [
        ("Månedligt salg", "Viser den samlede omsætning pr. måned. Bruges til at identificere vækstmønstre."),
        ("Top produkter", "De bedst sælgende produkter i perioden."),
        ("Top kunder", "Kunder med højest omsætning."),
        ("Salg pr. land", "Fordeling af salg på lande."),
        ("Gns. salgspris og COGS", "Gennemsnitlig salgspris og kostpris for top 10 produkter."),
        ("Profitprodukter", "Produkter med højest samlet profit."),
        ("Top produktfamilier", "Familier med størst omsætning."),
        ("Månedlig omsætning", "Omsætning grupperet pr. måned."),
        ("Antal ordrer", "Viser hvor mange ordrer der er lagt pr. måned."),
        ("Pris over tid", "Udviklingen i gennemsnitlig salgspris."),
        ("Ugedagsanalyse", "Hvilke ugedage performer bedst."),
        ("Salg pr. størrelse", "Hvilke størrelser sælger bedst."),
        ("Top familier", "Produktfamilier med højest salg."),
        ("Produkttrends", "Produkter med stigende eller faldende tendens."),
        ("Top kunder (bar)", "Topkunder i bar-graf."),
        ("Pareto-analyse", "80/20 fordeling af kunder vs. salg."),
        ("Salg pr. land (geo)", "Geografisk fordeling af omsætning."),
    ]

    # Opret PDF-klasse med footer
    class CustomPDF(FPDF):
        def footer(self):
            self.set_y(-15)
            self.set_font("Arial", "I", 8)
            self.cell(0, 10, f"Side {self.page_no()}/{{nb}}", align="C")

    pdf = CustomPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.alias_nb_pages()
    pdf.add_page()

    # Første side med intro
    pdf.set_font("Arial", "B", 20)
    pdf.cell(0, 15, "Salgsrapport", ln=True, align="C")
    pdf.set_font("Arial", size=12)
    pdf.ln(10)
    pdf.cell(0, 10, f"Kunde: {name}", ln=True)
    pdf.cell(0, 10, f"Dato: {datetime.now().strftime('%Y-%m-%d')}", ln=True)
    pdf.ln(10)
    pdf.multi_cell(0, 10, "Denne rapport giver overblik over virksomhedens salgsdata, nøgleprodukter, kunder og geografisk performance. Den er genereret automatisk baseret på jeres seneste data.")

    # Evt. indsæt logo
    logo_path = "logo.png"
    if os.path.exists(logo_path):
        pdf.image(logo_path, x=10, y=10, w=30)

    # Tilføj alle figurer med titler og tekster
    for (title, desc), img_path in zip(descriptions, image_paths):
        pdf.add_page()
        pdf.set_font("Arial", "B", 14)
        pdf.cell(0, 10, title, ln=True)
        pdf.set_font("Arial", size=11)
        pdf.multi_cell(0, 8, desc)
        pdf.image(img_path, x=10, y=40, w=180)

    # Gem og send
    output_path = os.path.join(REPORT_DIR, f"report_{customer_id}.pdf")
    pdf.output(output_path)

    send_email(
        to_address=email,
        subject="Din ugentlige salgsrapport",
        body="Hej!\n\nSe vedhæftede PDF med jeres nyeste salgsanalyse.\n\nBedste hilsner,\nData Consultant Team",
        attachment_path=output_path
    )

    return output_path

