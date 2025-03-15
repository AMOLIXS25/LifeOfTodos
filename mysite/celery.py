import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

app = Celery('mysite')

app.conf.beat_schedule = {
    'send-reminders-every-minute': {
        'task': 'todo.tasks.send_reminders',
        'schedule': crontab(minute='*/1'),
    },
}

# Print pour vérifier le broker utilisé
from django.conf import settings

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()