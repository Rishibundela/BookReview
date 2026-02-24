from celery import Celery
from src.mail import create_message, mail
import asyncio
from src.config import Config

celery_app = Celery('bookly')

celery_app.config_from_object('src.config')

@celery_app.task
def send_verification_email(email: str, token: str):

    link = f"http://{Config.DOMAIN}/api/v1/auth/verify/{token}"

    html_message = f"""
    <h1>Verify your Email</h1>
    <p>Please click this <a href="{link}">link</a>
    to verify your email</p>
    """

    message = create_message(
        recipients=[email],
        subject="Verify your email",
        body=html_message,
    )

    # Celery task is sync → FastAPI-Mail async
    asyncio.run(mail.send_message(message))

@celery_app.task
def send_password_reset_email(email: str, token: str):

    link = f"http://{Config.DOMAIN}/api/v1/auth/verify/{token}"

    html_message = f"""
    <h1>Reset your password</h1>
    <p>Please click this <a href="{link}">link</a>
    to reset your password</p>
    """

    message = create_message(
        recipients=[email],
        subject="Reset your password",
        body=html_message,
    )

    # Celery task is sync → FastAPI-Mail async
    asyncio.run(mail.send_message(message))
