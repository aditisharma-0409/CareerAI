import smtplib
import os
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()


def send_email(to_email, subject, message):

    sender_email = os.getenv("CAREERAI_EMAIL")
    sender_password = os.getenv("CAREERAI_EMAIL_PASSWORD")

    if not sender_email or not sender_password:
        print("Email credentials are not configured.")
        return False

    try:
        email = EmailMessage()

        email["From"] = sender_email
        email["To"] = to_email
        email["Subject"] = subject

        email.set_content(message)

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:

            smtp.login(
                sender_email,
                sender_password
            )

            smtp.send_message(email)

        print("Email sent successfully.")

        return True

    except Exception as e:

        print(f"Email sending failed: {e}")

        return False