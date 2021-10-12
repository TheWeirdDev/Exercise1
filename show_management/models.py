from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    CANDIDATE = 0
    MENTOR = 1
    ADMIN = 2

    ROLE_CHOICES = (
        (CANDIDATE, 'Candidate'),
        (MENTOR, 'Mentor'),
        (ADMIN, 'Admin'),
    )
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, default=CANDIDATE)

class Mentor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class Team(models.Model):
    mentor = models.ForeignKey(Mentor, on_delete=models.CASCADE)

class Candidate(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)

class Activity(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    date = models.DateField()
    average_score = models.FloatField(default=0)

class Score(models.Model):
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    mentor = models.ForeignKey(Mentor, on_delete=models.CASCADE)
    score = models.IntegerField()