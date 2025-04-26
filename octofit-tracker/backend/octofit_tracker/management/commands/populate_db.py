from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Leaderboard, Workout
from django.conf import settings
from pymongo import MongoClient
from datetime import timedelta
from bson import ObjectId

class Command(BaseCommand):
    help = 'Populate the database with test data for Merington High School fitness tracking'

    def handle(self, *args, **kwargs):
        # Connect to MongoDB
        client = MongoClient(settings.DATABASES['default']['HOST'], settings.DATABASES['default']['PORT'])
        db = client[settings.DATABASES['default']['NAME']]

        # Drop existing collections
        db.octofit_tracker_user.drop()
        db.octofit_tracker_team.drop()
        db.octofit_tracker_activity.drop()
        db.octofit_tracker_leaderboard.drop()
        db.octofit_tracker_workout.drop()

        # Create users
        users = [
            User(_id=ObjectId(), username='sarah_swim', email='sarah@merington.edu', password='sarah123'),
            User(_id=ObjectId(), username='track_master', email='mike@merington.edu', password='mike123'),
            User(_id=ObjectId(), username='yoga_queen', email='lisa@merington.edu', password='lisa123'),
            User(_id=ObjectId(), username='basketball_pro', email='james@merington.edu', password='james123'),
            User(_id=ObjectId(), username='soccer_star', email='emma@merington.edu', password='emma123'),
        ]
        User.objects.bulk_create(users)
        self.stdout.write(self.style.SUCCESS('Created users'))

        # Create teams
        teams = [
            Team(_id=ObjectId(), name='Merington Marlins'),
            Team(_id=ObjectId(), name='Fitness Warriors'),
        ]
        Team.objects.bulk_create(teams)
        
        # Add members to teams
        teams[0].members.add(users[0], users[1], users[2])
        teams[1].members.add(users[3], users[4])
        self.stdout.write(self.style.SUCCESS('Created teams and added members'))

        # Create activities
        activities = [
            Activity(_id=ObjectId(), user=users[0], activity_type='Swimming', duration=timedelta(hours=1)),
            Activity(_id=ObjectId(), user=users[1], activity_type='Track Running', duration=timedelta(minutes=45)),
            Activity(_id=ObjectId(), user=users[2], activity_type='Yoga', duration=timedelta(minutes=60)),
            Activity(_id=ObjectId(), user=users[3], activity_type='Basketball', duration=timedelta(hours=1, minutes=30)),
            Activity(_id=ObjectId(), user=users[4], activity_type='Soccer Practice', duration=timedelta(hours=2)),
        ]
        Activity.objects.bulk_create(activities)
        self.stdout.write(self.style.SUCCESS('Created activities'))

        # Create leaderboard entries
        leaderboard_entries = [
            Leaderboard(_id=ObjectId(), user=users[0], score=95),
            Leaderboard(_id=ObjectId(), user=users[1], score=88),
            Leaderboard(_id=ObjectId(), user=users[2], score=92),
            Leaderboard(_id=ObjectId(), user=users[3], score=85),
            Leaderboard(_id=ObjectId(), user=users[4], score=90),
        ]
        Leaderboard.objects.bulk_create(leaderboard_entries)
        self.stdout.write(self.style.SUCCESS('Created leaderboard entries'))

        # Create workouts
        workouts = [
            Workout(_id=ObjectId(), name='Swim Training', description='50m freestyle sprints and endurance laps'),
            Workout(_id=ObjectId(), name='Track Conditioning', description='400m repeats and sprint training'),
            Workout(_id=ObjectId(), name='Yoga Flow', description='60-minute vinyasa flow sequence'),
            Workout(_id=ObjectId(), name='Basketball Drills', description='Shooting, dribbling, and defensive exercises'),
            Workout(_id=ObjectId(), name='Soccer Skills', description='Passing, shooting, and agility drills'),
        ]
        Workout.objects.bulk_create(workouts)
        self.stdout.write(self.style.SUCCESS('Created workouts'))

        self.stdout.write(self.style.SUCCESS('Successfully populated all collections with test data'))