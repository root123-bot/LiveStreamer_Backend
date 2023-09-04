from LiveStreaming.assets.views import *
from django.conf.urls import url


urlpatterns = [
    url(r'matches/$', fetch_matches, name="matches"),
    url(r'manager/$', get_manager, name="manager"),
    url(r'teamPlayers/$', team_players, name="homePlayers"),
    url(r'venues/$', fetch_venues, name="venues"),
    url(r'teams/$', fetch_teams, name="teams"),
    url(r'players/$', fetch_players, name="players"),
    url(r'competitions/$', fetch_competition, name='competitions'),
    url(r'addMatch/$', create_match, name="new_match"),
    url(r'addPlayer/$', create_player, name="new_player"),
    url(r'addTeam/$', create_team, name='new_team'),
    url(r'addVenue/$', create_venue, name='new_venue'),
    url(r'addCompetition/$', create_competition, name='new_competition')
]