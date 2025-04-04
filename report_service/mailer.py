from email.message import EmailMessage
import smtplib
import os
from dotenv import load_dotenv

load_dotenv()

def send_email(to_address, subject, body, attachment_path=None):
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = os.getenv("EMAIL_SENDER")
    msg["To"] = to_address
    msg.set_content(body)

    if attachment_path:
        with open(attachment_path, "rb") as f:
            file_data = f.read()
            file_name = os.path.basename(attachment_path)
        msg.add_attachment(file_data, maintype="application", subtype="pdf", filename=file_name)

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(os.getenv("EMAIL_SENDER"), os.getenv("EMAIL_PASSWORD"))
            smtp.send_message(msg)
            print(f"✅ E-mail sendt til {to_address}")
    except Exception as e:
        print(f"❌ E-mail fejlede: {e}")

