# test_report_generator.py
from report_service.report_generator import generate_pdf_report

if __name__ == "__main__":
    path = generate_pdf_report("pilot001")
    print("Rapport gemt som:", path)
