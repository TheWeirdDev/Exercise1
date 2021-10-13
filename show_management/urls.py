from django.urls import path
from .views import home_page, list_teams, show_team
urlpatterns = [
    path('', home_page, name='home_page'),
    path('teams', list_teams, name='list_teams'),
    path('team/<int:team_id>/', show_team, name='show_team'),
]

app_name = 'show_management'