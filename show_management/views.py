from show_management.utils import is_mentor
from show_management.models import Team, User
from show_management.decorators import mentor_or_admin_required
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

LOGIN_URL = '/login'
@login_required(login_url=LOGIN_URL)
def home_page(request):
    if request.user.role == User.CANDIDATE:
        return render(request, 'candidate_home.html', {'candidate' : request.user.candidate})
    else:
        return redirect('list_teams')

@login_required(login_url=LOGIN_URL)
@mentor_or_admin_required
def list_teams(request):
    if is_mentor(request.user):
        teams = request.user.mentor.team_set.all()
    else:
        teams = Team.objects.all()
    return render(request, 'list_teams.html', {'teams': teams})


@login_required(login_url=LOGIN_URL)
@mentor_or_admin_required
def show_team(request, team_id):
    team = get_object_or_404(Team, pk=team_id)
    # Admin can vire any team
    if request.user.role == User.ADMIN:
        return render(request, 'show_team.html', {'team': team})
    # Mentor can only view his own teams
    elif request.user.role == User.MENTOR and team.mentor != request.user.mentor:
        return render(request, 'show_team.html', {'error_message': 'You are not the mentor of this team.'})
    return render(request, 'show_team.html',
                  {'team' : team})
