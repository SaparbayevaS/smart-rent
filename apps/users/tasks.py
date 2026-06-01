from datetime import datetime

from celery import shared_task


@shared_task
def send_welcome_email(email: str) -> str:
    print(f"[CELERY] Sending welcome email to {email}")
    return f"Email sent to {email}"


@shared_task
def generate_daily_analytics() -> str:
    print(f"[ANALYTICS] Running at {datetime.now()}")
    return "analytics generated"