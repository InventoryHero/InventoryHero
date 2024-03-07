import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class Mail:
    def __init__(self, smtp_config, app_url):
        self.smtp_user = smtp_config['username']
        self.smtp_password = smtp_config['password']
        self.smtp_server = smtp_config['server']
        self.smtp_port = smtp_config['port']
        self.sender_email = smtp_config['sender_email']
        self.app_url = app_url

    def send_registration_confirmation(self, to, confirmation_code):
        message = MIMEMultipart('alternative')
        message['From'] = self.sender_email
        message['To'] = to
        message['Subject'] = "Please confirm your email address"
        text = f"""\
        Hi, 
        
        please follow the link below to activate your account and start using InventoryHero!
        {self.app_url}/confirmation/{confirmation_code}
        
        Your InventoryHero Team!
        """

        html = f"""\
        <html>
            <body>
                <p> Hi, <br>
                    please click <a href="{self.app_url}/confirmation/{confirmation_code}">here</a> to activate your
                    account and start using InventoryHero! <br>
                    If you are not sure if the link embedded above is save here it is again in plain: 
                    {self.app_url}/confirmation/{confirmation_code} <br>
                    Your InventoryHero Team!
                <p>
            <body>
        <html>
        """
        part1 = MIMEText(text, "plain")
        part2 = MIMEText(html, "html")
        message.attach(part1)
        message.attach(part2)

        self.send_email(message, to)

    def send_email(self, message, to):
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(self.smtp_server, self.smtp_port, context=context) as server:
            server.login(self.smtp_user, self.smtp_password)
            server.sendmail(self.sender_email, to, message.as_string())


