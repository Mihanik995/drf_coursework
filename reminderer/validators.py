from datetime import datetime, timedelta, timezone, tzinfo

from rest_framework.validators import ValidationError


class BountyValidator:
    def __call__(self, attrs):
        if {'connected_habit', 'reward'}.issubset(attrs.keys()):
            if attrs['reward'] and attrs['connected_habit']:
                raise ValidationError({
                    "bounty": "You cannot have both the reward and connected pleasureful habit"
                })


class ExecutionTimeValidator:
    def __call__(self, attrs):
        if attrs['execution_time'] > timedelta(minutes=2):
            raise ValidationError({
                "execution_time": "Your habit's execution time cannot be more then 2 minutes"
            })


class ConnectedHabitValidator:
    def __call__(self, attrs):
        if {'connected_habit'}.issubset(attrs.keys()):
            if attrs['connected_habit'] and not attrs['connected_habit'].is_pleasureful:
                raise ValidationError({
                    "connected_habit": "Only pleasureful habits can be connected"
                })


class PleasurefulHabitsValidator:
    def __call__(self, attrs):
        if {'connected_habit', 'is_pleasureful', 'reward'}.issubset(attrs.keys()):
            if attrs['is_pleasureful'] and (attrs['connected_habit'] or attrs['reward']):
                raise ValidationError({
                    "bounty": "Pleasureful habits can have no reward or connected habit"
                })


class FrequencyValidator:
    def __call__(self, attrs):
        if 'frequency' in attrs.keys() and attrs['frequency'] > timedelta(days=7):
            raise ValidationError({
                "frequency": "Habit frequency cannot be more then 7 days"
            })


class TimeValidator:
    def __call__(self, attrs):
        if attrs['time'] < datetime.now(timezone.utc):
            raise ValidationError({
                'time': 'You cannot start the habit in the past'
            })
