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
        self.support_email = smtp_config.get('support_email', self.sender_email)
    def send_registration_confirmation(self, to, confirmation_code):
        message = MIMEMultipart('alternative')
        message['From'] = f"{self.sender_name} <{self.sender_email}>"
        message['To'] = to
        message['Subject'] = "Activate your InventoryHero account"
        url = f"{self.app_url}/confirmation/{confirmation_code}"

        # TODO USERINFO
        user_info = {
        }
        html = render_template(
            "/mail/account-activation.html",
            url=url,
            support_email=self.support_email,
            **user_info
        )

        message.attach(MIMEText(html, "html"))
        self.send_email(message, message['To'])

    def send_reset_password(self, to, reset_id):
        message = MIMEMultipart('alternative')
        message['From'] = f"{self.sender_name} <{self.sender_email}>"
        message['To'] = to["email"] # this needs to be present
        message['Subject'] = "Reset your InventoryHero password"
        url = f"{self.app_url}/password-reset/{reset_id}"
        user_info = {
            'first_name': to.get("first_name", None),
            'username': to.get("username", None)
        }
        html = render_template(
            "/mail/reset-password.html",
            url=url,
            support_email=self.support_email,
            **user_info
        )
        message.attach(MIMEText(html, "html"))
        self.send_email(message, message['To'])


    def send_email(self, message, to):
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(self.smtp_server, self.smtp_port, context=context) as server:
            server.login(self.smtp_user, self.smtp_password)
            server.sendmail(self.sender_email, to, message.as_string())


