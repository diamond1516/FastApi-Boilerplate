import ssl
from email.message import EmailMessage

import aiosmtplib
import certifi

from config import EMAIL_SETTINGS


async def send_email(
        recipient: str,
        subject: str,
        body: str = None,
        html_body: str = None,
        smtp_host: str = EMAIL_SETTINGS.EMAIL_HOST,
        smtp_port: int = EMAIL_SETTINGS.EMAIL_PORT,
        sender_email: str = EMAIL_SETTINGS.EMAIL,
        sender_password: str = EMAIL_SETTINGS.EMAIL_PASSWORD,
):
    """
    Sends an HTML email asynchronously.

    Args:
        smtp_host (str): SMTP server address (e.g., 'smtp.gmail.com').
        smtp_port (int): SMTP server port (e.g., 587 for TLS).
        sender_email (str): The email address of the sender.
        sender_password (str): The password for the sender's email.
        recipient (str): The email address of the recipient.
        subject (str): The subject of the email.
        html_body (str): The HTML content of the email.
        body (str): The plain text content for fallback (optional).

    Returns:
        None
    """

    assert html_body or body, 'The body or html body must be provided.'

    # Create an email message object
    message = EmailMessage()
    message["From"] = sender_email
    message["To"] = recipient
    message["Subject"] = subject

    # Add plain text part if provided
    if body:
        message.set_content(body)
    else:
        # Add HTML content
        message.add_alternative(html_body, subtype="html")

    # Create an SSL context with certifi
    ssl_context = ssl.create_default_context(cafile=certifi.where())

    # Send the email using aiosmtplib
    await aiosmtplib.send(
        message,
        hostname=smtp_host,
        port=smtp_port,
        username=sender_email,
        password=sender_password,
        start_tls=True,  # Use TLS for secure connection
        tls_context=ssl_context,
    )
