from report_service.report_generator import generate_pdf_report

if __name__ == "__main__":
    pdf_path = generate_pdf_report(customer_id="pilot001")
    print(f"PDF genereret: {pdf_path}")
