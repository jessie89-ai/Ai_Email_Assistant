import os
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")
SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT"))

def send_email(to_email, subject, body):
    """
    Sends an email reply using SMTP (Gmail).
    """
    try:
        # Create the email message
        msg = MIMEText(body, "plain")
        msg["Subject"] = subject
        msg["From"] = EMAIL
        msg["To"] = to_email

        # Connect to Gmail SMTP Server
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()  # Secure connection
            server.login(EMAIL, PASSWORD)
            server.sendmail(EMAIL, to_email, msg.as_string())

        print(f"✅ Email sent to {to_email} successfully!")

    except Exception as e:
        print("⚠️ Error sending email:", e)

# Test the function
if __name__ == "__main__":
    test_email = "recipient@example.com"  # Replace with an actual email for testing
    test_subject = "Re: Meeting Request"
    test_body = "Dear John,\n\nThanks for reaching out. Let's schedule a meeting next week!\n\nBest regards,\n[Your Name]"

    send_email(test_email, test_subject, test_body)
