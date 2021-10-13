from show_management.models import Activity
from django import template
from django.db.models import Avg, Sum
from ..utils import is_admin, is_mentor

register = template.Library()

@register.filter
def is_mentor(user):
    return is_mentor(user)


@register.filter
def is_admin(user):
    return is_admin(user)


@register.filter
def get_team_average_score(team):
    return team.candidate_set.aggregate(
        average_score=Avg('activity__average_score')
    )['average_score']


@register.filter
def get_candidate_average_score(candidate):
    return Activity.objects.filter(candidate=candidate).aggregate(
        average_score=Avg('average_score')
    )['average_score']
