from django.core.management.base import BaseCommand
from django.db.models import Avg

from show_management.models import Activity, User, Candidate, Mentor, Score, Team
from faker import Faker
import random
import tqdm

class Command(BaseCommand):
    NUM_USERS = 50

    def handle(self, *args, **options):
        print("Creating random data, this may take a while...")
        users = []
        f = Faker()
        a = tqdm.tqdm(desc="Creating users")
        a.total = self.NUM_USERS

        for i in range(Command.NUM_USERS):
            is_uniqe = False
            while not is_uniqe:
                username = f.name().lower().replace(' ', '')
                if not User.objects.filter(username=username).exists():
                    is_uniqe = True
                    new_user = User.objects.create_user(username=username,
                                                        email=f.email(),
                                                        password=f.password())
                    new_user.role = random.choices(
                        User.ROLE_CHOICES, [0.6, 0.2, 0.2])[0][0]
                    new_user.save()

                    if new_user.role == User.MENTOR:
                        a.total = a.total + 2
                        mentor = Mentor.objects.create(user=new_user)
                        mentor.save()
                    elif new_user.role == User.CANDIDATE:
                        a.total = a.total + 3
                    users.append(new_user)
                    a.update(1)

        a.set_description("Creating teams")
        # TODO: Make sure we have at least one mentor
        mentors = list(Mentor.objects.all())
        for i in range(len(mentors)*2):
            mentor = random.choice(mentors)
            mentor.team = Team.objects.create(mentor=mentor)
            mentor.save()
            a.update(1)

        a.set_description("Creating candidates")
        teams = list(Team.objects.all())
        for user in users:
            if user.role == User.CANDIDATE:
                team = random.choice(teams)
                candidate = Candidate.objects.create(user=user, team=team)
                candidate.save()
                a.update(1)

        a.set_description("Creating activities")
        candidates = list(Candidate.objects.all())
        for i in range(len(candidates) * 2):
            candidate = random.choice(candidates)
            activity_name = f.word()
            activity_date = f.date()
            activity = Activity.objects.create(
                candidate=candidate,
                name=activity_name,
                date=activity_date)
            activity.save()

            for mentor in mentors:
                score = Score.objects.create(
                    mentor=mentor,
                    activity=activity,
                    score=random.randint(0, 100))
                score.save()
            activity.average_score = Score.objects.filter(
                activity=activity).aggregate(Avg('score'))['score__avg']
            activity.save()
            a.update(1)