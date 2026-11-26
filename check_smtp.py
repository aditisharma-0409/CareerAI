
import os
import smtplib
import socket
import ssl
from dotenv import load_dotenv

load_dotenv()

email = os.getenv("CAREERAI_EMAIL", "").strip()
password = os.getenv("CAREERAI_EMAIL_PASSWORD", "").replace(" ", "").strip()


class IPv4SMTP_SSL(smtplib.SMTP_SSL):

    def _get_socket(self, host, port, timeout):
        ipv4_address = socket.gethostbyname(host)

        sock = socket.create_connection(
            (ipv4_address, port),
            timeout,
            self.source_address
        )

        return self.context.wrap_socket(
            sock,
            server_hostname=host
        )


try:
    print("Connecting through IPv4...")

    with IPv4SMTP_SSL("smtp.gmail.com", 465, timeout=30) as smtp:
        print("IPv4 connection established.")

        smtp.login(email, password)

        print("SUCCESS: Gmail authentication completed!")

except Exception as error:
    print("Test failed:")
    print(type(error).__name__, error)
