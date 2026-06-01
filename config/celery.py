import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('smart-rent')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    "daily-analytics": {
        "task": "apps.users.tasks.generate_daily_analytics",
        "schedule": crontab(minute=0, hour=0),
    },
}