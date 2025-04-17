import os
from io import BytesIO
from datetime import datetime
from fpdf import FPDF
from PyPDF2 import PdfMerger, PdfReader
from report_service.mailer import send_email
from report_service.customer_manager import get_customer_info
from scripts.load_data import load_accounts, load_plant_hierarchy, load_sales_data
from scripts.preprocess import convert_date_column, join_data
from pathlib import Path
from scripts.analysis import (
    plot_monthly_sales, top_products_by_sales, top_customers, sales_by_country,
    avg_price_and_cost, product_profit_margin, top_product_families, calculate_key_metrics
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

LOGO_PATH = Path("utills/klarlogo.jpeg")

def generate_figures(df, prefix):
    image_paths = []

    def save(fig_func, *args, suffix, **kwargs):
        path = os.path.join(REPORT_DIR, f"{prefix}_{suffix}.png")
        fig_func(*args, save_path=path, **kwargs)
        image_paths.append((suffix, path))

    save(plot_monthly_sales, df, suffix="monthly_sales")
    save(top_products_by_sales, df, suffix="top_products")
    save(top_customers, df, suffix="top_customers")
    save(sales_by_country, df, suffix="sales_by_country")
    save(avg_price_and_cost, df, suffix="avg_price_cost")
    save(product_profit_margin, df, suffix="profit_products")
    save(top_product_families, df, suffix="top_families")
    save(tp.plot_series, tm.sales_over_time(df, "M"), "Månedlig omsætning", "Måned", "USD", suffix="time_monthly_sales")
    save(tp.plot_series, tm.order_counts_over_time(df, "M"), "Ordrer pr. måned", "Måned", "Antal ordrer", suffix="time_orders")
    save(tp.plot_series, tm.avg_price_over_time(df, "M"), "Gns. pris over tid", "Måned", "USD", suffix="avg_price_over_time")
    save(tp.plot_series, tm.sales_by_weekday(df), "Omsætning pr. ugedag", "Ugedag", "USD", suffix="weekday_sales")
    save(pp.plot_bar_series, pm.sales_by_product_size(df), "Salg pr. størrelse", "Størrelse", "USD", suffix="product_size_sales")
    save(pp.plot_bar_series, pm.sales_by_family(df).head(10), "Top familier", "Familie", "USD", suffix="product_families")
    save(pp.plot_trend, pm.product_sales_trend(df), "Produkttrends", "Måned", "Salg i USD", suffix="product_trends")
    save(cp.plot_bar, cm.top_customers_by_sales(df), "Top kunder", "Kunde", "USD", suffix="top_customers_by_sales")
    save(cp.plot_line, cm.pareto_analysis(df), "Pareto (80/20)", "Kunde (sorteret)", "Andel", suffix="pareto")
    save(gp.plot_country_sales, gm.sales_by_country(df), suffix="geo_sales_by_country")

    return image_paths

def add_key_metrics_page(pdf, metrics):
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Nøglemetrics", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.ln(5)
    pdf.multi_cell(0, 8, (
        "Herunder ses en opsummering af de vigtigste salgsnøgletal for den analyserede periode."
    ))
    pdf.ln(5)
    col1, col2 = 60, 100
    pdf.cell(col1, 10, "Total omsætning:", ln=0)
    pdf.cell(col2, 10, f"{metrics['total_sales']:,} USD", ln=1)
    pdf.cell(col1, 10, "Antal ordrer:", ln=0)
    pdf.cell(col2, 10, str(metrics['total_orders']), ln=1)
    pdf.cell(col1, 10, "Gennemsnitlig pris:", ln=0)
    pdf.cell(col2, 10, f"{metrics['avg_price']:.2f} USD", ln=1)
    pdf.cell(col1, 10, "Top kunde:", ln=0)
    pdf.cell(col2, 10, f"{metrics['top_customer']} ({metrics['top_customer_sales']:,} USD)", ln=1)
    pdf.cell(col1, 10, "Top produkt:", ln=0)
    pdf.cell(col2, 10, f"{metrics['top_product']} ({metrics['top_product_sales']:,} USD)", ln=1)
    pdf.cell(col1, 10, "Andel fra top 10 kunder:", ln=0)
    pdf.cell(col2, 10, f"{metrics['top_10_pct']}%", ln=1)

def add_table_of_contents(pdf, toc_entries):
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Indholdsfortegnelse", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.ln(5)
    for i, (title, page_num) in enumerate(toc_entries, 1):
        dots = "." * (50 - len(title))
        line = f"{i}. {title} {dots} {page_num}"
        pdf.cell(0, 8, line, ln=True)

def add_chapter_page(pdf, title):
    pdf.add_page()
    pdf.set_fill_color(240, 240, 240)
    pdf.rect(0, 0, 210, 297, 'F')  # lys baggrund (A4)
    pdf.set_font("Arial", "B", 24)
    pdf.set_text_color(30, 30, 30)
    pdf.set_y(120)
    pdf.cell(0, 20, title, ln=True, align="C")
    pdf.set_text_color(0, 0, 0)

def generate_pdf_report(customer_id):
    customer = get_customer_info(customer_id)
    if not customer:
        raise ValueError(f"Kunde med id '{customer_id}' findes ikke.")
    name = customer["name"]
    email = customer["email"]

    accounts = load_accounts()
    products = load_plant_hierarchy()
    sales = load_sales_data()
    sales = convert_date_column(sales)
    merged_df = join_data(sales, accounts, products)
    metrics = calculate_key_metrics(merged_df)
    image_paths = generate_figures(merged_df, prefix=customer_id)

    descriptions = [
        ("Månedligt salg", "Viser den samlede omsætning pr. måned."),
        ("Top produkter", "De bedst sælgende produkter i perioden."),
        ("Top kunder", "Kunder med højest omsætning."),
        ("Salg pr. land", "Fordeling af salg på lande."),
        ("Gns. salgspris og COGS", "Gennemsnitlig salgspris og kostpris."),
        ("Profitprodukter", "Produkter med højest samlet profit."),
        ("Top produktfamilier", "Familier med størst omsætning."),
        ("Månedlig omsætning", "Omsætning pr. måned."),
        ("Antal ordrer", "Antal ordrer pr. måned."),
        ("Pris over tid", "Udvikling i gennemsnitspris."),
        ("Ugedagsanalyse", "Hvilke ugedage performer bedst."),
        ("Salg pr. størrelse", "Størrelser med højest salg."),
        ("Top familier", "Topproduktfamilier."),
        ("Produkttrends", "Udvikling i produkter over tid."),
        ("Top kunder (bar)", "Visuel fordeling af topkunder."),
        ("Pareto-analyse", "80/20 fordeling af kunder og salg."),
        ("Salg pr. land (geo)", "Geografisk fordeling."),
    ]

    class CustomPDF(FPDF):
        def footer(self):
            self.set_y(-15)
            self.set_font("Arial", "I", 8)
            self.cell(0, 10, f"Side {self.page_no()}/{{nb}}", align="C")

    pdf = CustomPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.alias_nb_pages()
    pdf.add_page()

    # Forside
    if LOGO_PATH.exists():
        pdf.image(str(LOGO_PATH), x=80, y=20, w=50)
    else:
        print("⚠️ Logo ikke fundet:", LOGO_PATH.resolve())

    pdf.ln(60)
    pdf.set_font("Arial", "B", 20)
    pdf.cell(0, 15, "Salgsrapport", ln=True, align="C")
    pdf.set_font("Arial", size=12)
    pdf.ln(10)
    pdf.cell(0, 10, f"Kunde: {name}", ln=True)
    pdf.cell(0, 10, f"Dato: {datetime.now().strftime('%Y-%m-%d')}", ln=True)
    pdf.ln(10)
    pdf.multi_cell(0, 10, "Denne rapport giver overblik over virksomhedens salgsdata og performance.")

    toc_entries = [("Nøglemetrics", pdf.page_no() + 1)]
    add_key_metrics_page(pdf, metrics)

    # Kapitelopdeling
    chapter_structure = {
        "1. Generelt overblik": [0, 1, 2, 3, 4, 5, 6],
        "2. Tidsbaseret analyse": [7, 8, 9, 10],
        "3. Produktanalyse": [11, 12, 13],
        "4. Kundesegmentering": [14, 15],
        "5. Geografisk fordeling": [16]
    }

    for chapter_title, indices in chapter_structure.items():
        add_chapter_page(pdf, chapter_title)
        toc_entries.append((chapter_title, pdf.page_no()))
        for i in indices:
            (title, desc), (suffix, img_path) = descriptions[i], image_paths[i]
            pdf.add_page()
            toc_entries.append((title, pdf.page_no()))
            pdf.set_font("Arial", "B", 14)
            pdf.cell(0, 10, title, ln=True)
            pdf.set_font("Arial", size=11)
            pdf.multi_cell(0, 8, desc)
            pdf.image(img_path, x=10, y=40, w=180)

    # Midlertidig PDF
    tmp_path = "_tmp_report.pdf"
    pdf.output(tmp_path)

    # Indholdsfortegnelse separat
    toc_pdf = FPDF()
    toc_pdf.set_auto_page_break(auto=True, margin=15)
    toc_pdf.alias_nb_pages()
    add_table_of_contents(toc_pdf, toc_entries)
    toc_stream = BytesIO(toc_pdf.output(dest='S').encode("latin1"))

    # Merge: Forside + ToC + resten
    merger = PdfMerger()
    merger.append(tmp_path, pages=(0, 1))
    merger.append(toc_stream)
    total_pages = len(PdfReader(tmp_path).pages)
    merger.append(tmp_path, pages=(1, total_pages))

    output_path = os.path.join(REPORT_DIR, f"report_{customer_id}.pdf")
    with open(output_path, "wb") as f:
        merger.write(f)

    send_email(
        to_address=email,
        subject="Din ugentlige salgsrapport",
        body="""
        Hej!

        Se vedhæftede PDF med jeres nyeste salgsanalyse.

        Bedste hilsner,
        Data Consultant Team
        """,
        attachment_path=output_path
    )

    return output_path

