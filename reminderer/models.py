from datetime import timedelta

from django.db import models

from users.models import User, NULLABLE

HABIT_MODEL = 'reminderer.Habit'

class Habit(models.Model):
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)

    place = models.CharField(max_length=100)
    time = models.DateTimeField()
    action = models.CharField(max_length=100)
    frequency = models.DurationField(default=timedelta(days=1))
    execution_time = models.DurationField()
    is_public = models.BooleanField(default=False)
    is_pleasureful = models.BooleanField(default=False)

    connected_habit = models.ForeignKey(to=HABIT_MODEL, on_delete=models.SET_NULL, **NULLABLE)
    reward = models.CharField(max_length=200, **NULLABLE)

    def __str__(self):
        return f"{self.action} in {self.place} at {self.time}"

    class Meta:
        verbose_name = 'habit'
        verbose_name_plural = 'habits'
