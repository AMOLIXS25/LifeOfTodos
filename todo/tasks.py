from celery import shared_task
from django.core.mail import send_mail
from datetime import datetime, timedelta
from .models import Reminder

@shared_task
def send_reminders():
    now_plus_one_hour = datetime.now() + timedelta(hours=1)
    reminders = Reminder.objects.filter(reminder_at__lte=now_plus_one_hour, sent=False)
    print(now_plus_one_hour)
    if len(reminders) > 0:
        for reminder in reminders:
            # Envoyer un e-mail
            send_mail(
                '🔔 Rappel LifeOfTodos',
                f"N'oublie pas d'accomplir cette todo : {reminder.task.title}",
                'kaliroot08@gmail.com',
                [reminder.user.email],
                fail_silently=False,
            )

            # Marquer comme envoyé
            reminder.sent = True
            reminder.save()