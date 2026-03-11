# celery_app.py
from celery import Celery
from celery.schedules import crontab
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

celery = Celery(
    'ppa',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/0'
)

celery.conf.update(
    timezone='Asia/Kolkata',
    enable_utc=True,
)

celery.conf.beat_schedule = {
    'send-daily-reminders': {
        'task': 'celery_app.send_daily_reminders',
        'schedule': crontab(hour=8, minute=0),
    },
    'send-monthly-report': {
        'task': 'celery_app.send_monthly_report',
        'schedule': crontab(day_of_month=1, hour=6, minute=0),
    },
}
celery.autodiscover_tasks(['tasks'])