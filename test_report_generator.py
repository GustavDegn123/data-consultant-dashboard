from report_service.report_generator import generate_pdf_report

if __name__ == "__main__":
    path = generate_pdf_report("demo001")
    print("✅ Rapport genereret:", path)
