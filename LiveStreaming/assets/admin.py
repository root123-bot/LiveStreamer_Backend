from django.contrib import admin
from .models import Venue, Team, Competition, Player, Match, TeamManager
# Register your models here.
admin.site.register(Venue)
admin.site.register(Team)
admin.site.register(Competition)
admin.site.register(Player)
admin.site.register(Match)
admin.site.register(TeamManager)
