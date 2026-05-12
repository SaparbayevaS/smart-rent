from celery import shared_task
from datetime import datetime

@shared_task
def send_welcome_email(email):
    print(f"[CELERY]Sending welcome email to {email}")
    return f"Email sent to {email}"

@shared_task
def generate_daily_analytics():
    print(f"[ANALYTICS] Running at {datetime.now()}")
    return "analytics generated"
