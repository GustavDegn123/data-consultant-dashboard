# filepath: /Users/gustavdegn/Documents/Data Consultant Project/test_report_generator.py
from report_service.report_generator import generate_pdf_report

if __name__ == "__main__":
    pdf_path = generate_pdf_report(customer_name="TestKunde")
    print(f"PDF genereret: {pdf_path}")