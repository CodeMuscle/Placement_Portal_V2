# mail.py
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging

logger = logging.getLogger(__name__)

def send_email(to_email, subject, body, is_html=False):
    msg = MIMEMultipart()
    msg['From'] = 'ppa@institute.com'
    msg['To'] = to_email
    msg['Subject'] = subject

    mime_type = 'html' if is_html else 'plain'
    msg.attach(MIMEText(body, mime_type))

    try:
        with smtplib.SMTP(host='localhost', port=1025) as smtp:
            smtp.send_message(msg)
        logger.info(f"Email sent successfully to {to_email}")
    except (smtplib.SMTPException, ConnectionRefusedError) as e:
        logger.warning(f"Failed to send email to {to_email}: {str(e)}")
