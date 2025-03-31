import os
import matplotlib.pyplot as plt
from fpdf import FPDF
from datetime import datetime
from report_service.mailer import send_email
from scripts.load_data import load_accounts, load_plant_hierarchy, load_sales_data
from scripts.preprocess import convert_date_column, join_data
from scripts.analysis import (
    plot_monthly_sales,
    top_products_by_sales,
    top_customers,
    sales_by_country,
    avg_price_and_cost,
    product_profit_margin
)

REPORT_DIR = "generated_reports"
os.makedirs(REPORT_DIR, exist_ok=True)

def generate_figures(df):
    figs = []
    figs.append(plot_monthly_sales(df))
    figs.append(top_products_by_sales(df))
    figs.append(top_customers(df))
    figs.append(sales_by_country(df))
    figs.append(avg_price_and_cost(df))
    figs.append(product_profit_margin(df))
    return figs

def save_figures_as_images(figs, prefix):
    paths = []
    for i, fig in enumerate(figs):
        path = os.path.join(REPORT_DIR, f"{prefix}_fig{i+1}.png")
        fig.savefig(path)
        paths.append(path)
        plt.close(fig)
    return paths

def generate_pdf_report(customer_name="Pilotkunde"):
    # Load and merge data
    accounts = load_accounts()
    products = load_plant_hierarchy()
    sales = load_sales_data()
    sales = convert_date_column(sales)
    merged_df = join_data(sales, accounts, products)

    # Generate figures and save as images
    figs = generate_figures(merged_df)
    image_paths = save_figures_as_images(figs, customer_name)

    # Create PDF
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, f"Salgsrapport for {customer_name}", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, f"Dato: {datetime.now().strftime('%Y-%m-%d')}", ln=True)

    for img_path in image_paths:
        pdf.add_page()
        pdf.image(img_path, x=10, y=30, w=180)

    output_path = os.path.join(REPORT_DIR, f"report_{customer_name}.pdf")
    pdf.output(output_path)

    # Optionally send email
    send_email(to_address="pilot@example.com", subject="Din ugentlige salgsrapport", body="Se vedhæftede PDF", attachment_path=output_path)

    return output_path
