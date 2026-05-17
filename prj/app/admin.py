from django.contrib import admin
from .models import RiotAccount, Match, Player, MatchParticipant, Agent, Map

@admin.register(RiotAccount)
class RiotAccountAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "region", "puuid", "last_synced_at")
    search_fields = ("puuid", "user__username")

@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ("id", "riot_match_id", "started_at", "map")
    search_fields = ("riot_match_id",)
    list_filter = ("map",)

@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ("id", "puuid", "game_name", "tag_line")
    search_fields = ("puuid", "game_name", "tag_line")

@admin.register(MatchParticipant)
class MatchParticipantAdmin(admin.ModelAdmin):
    list_display = ("id", "match", "player", "team", "agent", "kills", "deaths", "assists", "acs")
    search_fields = ("match__riot_match_id", "player__puuid")
    list_filter = ("team", "agent")

admin.site.register(Agent)
admin.site.register(Map)