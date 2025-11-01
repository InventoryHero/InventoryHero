from typing import Optional

from ih.core.config import get_app_settings
from ih.core.logging.logger import get_logger
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, select_autoescape
from email.message import EmailMessage
import smtplib
from datetime import datetime

settings = get_app_settings()
logger = get_logger()

template_dir = Path(__file__).parent / "templates"



def send_confirmation_email(to: str, username: str, reset_code: str) -> bool:
    """
    Sends a password reset email using Jinja2 HTML template.
    """

    if not settings.IH_SMTP_ENABLED:
        return False
    env = Environment(
        loader=FileSystemLoader(template_dir),
        autoescape=select_autoescape(["html", "xml"])
    )

    template = env.get_template("standard.html")

    html_content = template.render(
        subject="Confirm your E-Mail",
        title="Inventory Hero",
        logo_url="https://raw.githubusercontent.com/InventoryHero/InventoryHero/15c18f9d54ff042c41d9747a7b946aa99c9d80ed/frontend/public/android-chrome-512x512.png", # TODO
        username=username,  # You’d pass the actual username here
        upper_part="Thanks for trusting InventoryHero. To get you started you need to confirm your e-mail address by clicking below.",
        btn={
            "text": "Confirm E-Mail",
            "href": f"{settings.IH_APP_URL}/confirm/{reset_code}"
        },
        lower_part="",
        current_year=datetime.now().year,
        website_url=settings.IH_APP_URL
    )

    msg = EmailMessage()
    msg["Subject"] = "Confirm your E-Mail"
    msg["From"] = f"{settings.IH_SMTP_FROM_NAME} <{settings.IH_SMTP_FROM_EMAIL}>"
    msg["To"] = to
    msg.set_content("Please view this email in HTML format.")  # plain text fallback
    msg.add_alternative(html_content, subtype="html")

    try:
        with smtplib.SMTP(settings.IH_SMTP_HOST, settings.IH_SMTP_PORT) as server:
            # TODO LOGIN, SSL/TLS
            # TODO confirmation view
            #smtp.login("no-reply@inventoryhero.app", "YOUR_APP_PASSWORD")
            server.send_message(msg)
        logger.info(f"Email confirmation email sent to {to}")
        return True
    except Exception as e:
        logger.error(f"Failed to send email: {e}")
        return False



def send_password_reset_email(to: str, username: str, reset_url: str, admin_username: Optional[str] = None) -> bool:
    """
    Sends a password reset email using Jinja2 HTML template.
    """
    from_admin = admin_username is not None
    if not settings.IH_SMTP_ENABLED:
        return False
    env = Environment(
        loader=FileSystemLoader(template_dir),
        autoescape=select_autoescape(["html", "xml"])
    )

    template = env.get_template("standard.html")

    html_content = template.render(
        subject="Reset your password",
        title="Inventory Hero",
        logo_url="https://raw.githubusercontent.com/InventoryHero/InventoryHero/15c18f9d54ff042c41d9747a7b946aa99c9d80ed/frontend/public/android-chrome-512x512.png", # TODO
        username=username,  # You’d pass the actual username here
        upper_part=(
            f"The administrator {admin_username} has generated this password reset code for you."
            if from_admin
            else "You requested a password reset. Use the code below to reset your password."
        ),
        btn={
            "text": "Reset Password",
            "href": reset_url
        },
        lower_part=(
            "If you did not request this reset you can safely ignore this email"
            if not from_admin
            else "If you did not expect this, you should immediately request a new password reset link from the login form."
        ),
        current_year=datetime.now().year,
        website_url=settings.IH_APP_URL
    )

    msg = EmailMessage()
    msg["Subject"] = "Reset your InventoryHero password"
    msg["From"] = f"{settings.IH_SMTP_FROM_NAME} <{settings.IH_SMTP_FROM_EMAIL}>"
    msg["To"] = to
    msg.set_content("Please view this email in HTML format.")  # plain text fallback
    msg.add_alternative(html_content, subtype="html")

    try:
        with smtplib.SMTP(settings.IH_SMTP_HOST, settings.IH_SMTP_PORT) as server:
            # TODO LOGIN, SSL/TLS
            # TODO confirmation view
            #smtp.login("no-reply@inventoryhero.app", "YOUR_APP_PASSWORD")
            server.send_message(msg)
        logger.info(f"Password reset email sent to {to}")
        return True
    except Exception as e:
        logger.error(f"Failed to send password reset email: {e}")
        return False
