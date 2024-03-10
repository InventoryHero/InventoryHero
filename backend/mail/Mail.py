import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from flask import render_template


class Mail:
    def __init__(self, smtp_config, app_url):
        self.smtp_user = smtp_config['username']
        self.smtp_password = smtp_config['password']
        self.smtp_server = smtp_config['server']
        self.smtp_port = smtp_config['port']
        self.sender_email = smtp_config['from_email']
        self.sender_name = smtp_config['from_name']
        self.app_url = app_url

    def send_registration_confirmation(self, to, confirmation_code):
        message = MIMEMultipart('alternative')
        message['From'] = f"{self.sender_name} <{self.sender_email}>"
        message['To'] = to
        message['Subject'] = "Please confirm your email address"
        url = f"{self.app_url}/confirmation/{confirmation_code}"

        html = render_template("/mail/register.html", url=url)
        message.attach(MIMEText(html, "html"))
        self.send_email(message, to)

    def send_email(self, message, to):
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(self.smtp_server, self.smtp_port, context=context) as server:
            server.login(self.smtp_user, self.smtp_password)
            server.sendmail(self.sender_email, to, message.as_string())


