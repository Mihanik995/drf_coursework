from datetime import datetime, timezone, timedelta

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.validators import ValidationError

from reminderer.models import Habit
from users.models import User


class HabitTestCase(APITestCase):
    def setUp(self):
        self.test_user = User.objects.create(email='test@mail.com')
        self.test_user.set_password('123test456')
        self.test_user.save()

        self.client.force_authenticate(user=self.test_user)

        self.test_useful_habit = Habit.objects.create(
            owner=self.test_user,
            place='test place',
            time=datetime.now(timezone.utc) + timedelta(days=10),
            action='test action',
            execution_time=timedelta(minutes=1)
        )

        self.test_pleasureful_habit = Habit.objects.create(
            owner=self.test_user,
            place='test nasty place',
            time=datetime.now(timezone.utc) + timedelta(days=10),
            action='test reward action',
            execution_time=timedelta(minutes=1),
            is_pleasureful=True
        )

    def test_list(self):
        response = self.client.get('/habits/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['count'], 2)

    def test_retrieve(self):
        response = self.client.get(f'/habits/{self.test_useful_habit.pk}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['place'], 'test place')

    def test_post(self):
        response = self.client.post('/habits/', {
            'place': 'another test place',
            'time': datetime.now(timezone.utc) + timedelta(hours=1),
            'action': 'another test action',
            'execution_time': timedelta(minutes=1),
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Habit.objects.filter(place='another test place').exists())

    def test_update(self):
        response = self.client.put(f'/habits/{self.test_useful_habit.pk}/', {
            'place': self.test_useful_habit.place,
            'time': self.test_useful_habit.time,
            'action': self.test_useful_habit.action,
            'execution_time': self.test_useful_habit.execution_time,

            'reward': 'candy'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Habit.objects.get(pk=self.test_useful_habit.pk).reward, 'candy')

    def test_destroy(self):
        response = self.client.delete(f'/habits/{self.test_useful_habit.pk}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertTrue(not Habit.objects.filter(pk=self.test_useful_habit.pk).exists())

    def test_bounty_validator(self):
        self.client.put(f'/habits/{self.test_useful_habit.pk}/', {
            'place': self.test_useful_habit.place,
            'time': self.test_useful_habit.time,
            'action': self.test_useful_habit.action,
            'execution_time': self.test_useful_habit.execution_time,

            'reward': 'candy',
            'connected_habit': self.test_pleasureful_habit.pk
        })
        self.assertRaises(ValidationError, msg={
            "bounty": "You cannot have both the reward and connected pleasureful habit"
        })

    def test_execution_time_validator(self):
        self.client.put(f'/habits/{self.test_useful_habit.pk}/', {
            'place': self.test_useful_habit.place,
            'time': self.test_useful_habit.time,
            'action': self.test_useful_habit.action,

            'execution_time': timedelta(minutes=3)
        })
        self.assertRaises(ValidationError, msg={
            "execution_time": "Your habit's execution time cannot be more then 2 minutes"
        })

    def test_connected_habit_validator(self):
        self.client.put(f'/habits/{self.test_useful_habit.pk}/', {
            'place': self.test_useful_habit.place,
            'time': self.test_useful_habit.time,
            'action': self.test_useful_habit.action,
            'execution_time': self.test_useful_habit.execution_time,

            'connected_habit': self.test_useful_habit.pk
        })
        self.assertRaises(ValidationError, msg={
            "connected_habit": "Only pleasureful habits can be connected"
        })

    def test_pleasureful_habits_validator(self):
        self.client.put(f'/habits/{self.test_pleasureful_habit.pk}/', {
            'place': self.test_useful_habit.place,
            'time': self.test_useful_habit.time,
            'action': self.test_useful_habit.action,
            'execution_time': self.test_useful_habit.execution_time,

            'connected_habit': self.test_useful_habit.pk
        })
        self.assertRaises(ValidationError, msg={
            "bounty": "Pleasureful habits can have no reward or connected habit"
        })

        self.client.put(f'/habits/{self.test_pleasureful_habit.pk}/', {
            'place': self.test_useful_habit.place,
            'time': self.test_useful_habit.time,
            'action': self.test_useful_habit.action,
            'execution_time': self.test_useful_habit.execution_time,

            'reward': 'candy'
        })
        self.assertRaises(ValidationError, msg={
            "bounty": "Pleasureful habits can have no reward or connected habit"
        })

    def test_frequency_validator(self):
        self.client.put(f'/habits/{self.test_useful_habit.pk}/', {
            'place': self.test_useful_habit.place,
            'time': self.test_useful_habit.time,
            'action': self.test_useful_habit.action,
            'execution_time': self.test_useful_habit.execution_time,

            'frequency': timedelta(days=10)
        })
        self.assertRaises(ValidationError, msg={
            "frequency": "Habit frequency cannot be more then 7 days"
        })

    def test_time_validator(self):
        self.client.put(f'/habits/{self.test_useful_habit.pk}/', {
            'place': self.test_useful_habit.place,
            'action': self.test_useful_habit.action,
            'execution_time': self.test_useful_habit.execution_time,

            'time': datetime.now(timezone.utc) - timedelta(days=1)
        })
        self.assertRaises(ValidationError, msg={
            'time': 'You cannot start the habit in the past'
        })
