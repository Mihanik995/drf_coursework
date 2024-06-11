from datetime import timedelta

from celery import shared_task
from django.utils import timezone

from reminderer.models import Habit
from reminderer.scripts import send_reminder


@shared_task
def check_habits_for_reminder_requirements():
    for habit in Habit.objects.filter(is_pleasureful=False).all():
        current_time = timezone.now()
        if current_time < habit.time < current_time + timedelta(minutes=10):
            send_reminder(habit)
