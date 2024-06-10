from datetime import timedelta

from rest_framework import serializers

from reminderer.models import Habit
from reminderer.validators import BountyValidator, ExecutionTimeValidator, ConnectedHabitValidator, \
    PleasurefulHabitsValidator, FrequencyValidator, TimeValidator


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = '__all__'
        validators = [
            BountyValidator(),
            ExecutionTimeValidator(),
            ConnectedHabitValidator(),
            PleasurefulHabitsValidator(),
            FrequencyValidator(),
            TimeValidator()
        ]

    def create(self, validated_data):
        new_habit = Habit.objects.create(**validated_data)
        new_habit.owner = self.context.get('request').user
        new_habit.save()

        return new_habit
