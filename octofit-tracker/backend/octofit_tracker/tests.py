from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import User, Team, Activity, Leaderboard, Workout
from datetime import timedelta

class ModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.team = Team.objects.create(name='Test Team')
        self.team.members.add(self.user)
        self.activity = Activity.objects.create(
            user=self.user,
            activity_type='running',
            duration=timedelta(minutes=30)
        )
        self.leaderboard = Leaderboard.objects.create(
            user=self.user,
            score=100
        )
        self.workout = Workout.objects.create(
            name='Test Workout',
            description='Test workout description',
            difficulty='intermediate'
        )

    def test_user_creation(self):
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.email, 'test@example.com')

    def test_team_creation(self):
        self.assertEqual(self.team.name, 'Test Team')
        self.assertEqual(self.team.members.count(), 1)

    def test_activity_creation(self):
        self.assertEqual(self.activity.activity_type, 'running')
        self.assertEqual(self.activity.duration, timedelta(minutes=30))

    def test_leaderboard_creation(self):
        self.assertEqual(self.leaderboard.score, 100)
        self.assertEqual(self.leaderboard.user, self.user)

    def test_workout_creation(self):
        self.assertEqual(self.workout.name, 'Test Workout')
        self.assertEqual(self.workout.difficulty, 'intermediate')

class APITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.team = Team.objects.create(name='Test Team')
        self.team.members.add(self.user)

    def test_api_root(self):
        response = self.client.get(reverse('api-root'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('users', response.data)
        self.assertIn('teams', response.data)
        self.assertIn('activities', response.data)
        self.assertIn('leaderboard', response.data)
        self.assertIn('workouts', response.data)

    def test_list_users(self):
        response = self.client.get(reverse('user-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_activity(self):
        response = self.client.post(reverse('activity-list'), {
            'user': self.user.id,
            'activity_type': 'running',
            'duration': '00:30:00'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Activity.objects.count(), 1)