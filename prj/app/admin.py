from django.contrib import admin
from app.models import Player, Match, MatchStats

admin.site.register(MatchStats)
admin.site.register(Player)
admin.site.register(Match)