from django.conf import settings
from django.db import models

class RiotAccount(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    puuid = models.CharField(max_length=128, unique=True)
    region = models.CharField(max_length=16)  # e.g. eu, na, ap, kr (depends on API)
    last_synced_at = models.DateTimeField(null=True, blank=True)

class Map(models.Model):
    riot_map_id = models.CharField(max_length=64, unique=True)  # or just name unique
    name = models.CharField(max_length=64)

class Agent(models.Model):
    riot_agent_id = models.CharField(max_length=64, unique=True)
    name = models.CharField(max_length=64)

class Match(models.Model):
    riot_match_id = models.CharField(max_length=64, unique=True)
    started_at = models.DateTimeField(null=True, blank=True)
    game_version = models.CharField(max_length=64, blank=True, default="")
    queue_id = models.CharField(max_length=32, blank=True, default="")  # if available
    map = models.ForeignKey(Map, null=True, blank=True, on_delete=models.SET_NULL)

class Player(models.Model):
    puuid = models.CharField(max_length=128, unique=True)
    # privacy-friendly: omit name/tag. If you store it, keep it optional.
    game_name = models.CharField(max_length=64, blank=True, default="")
    tag_line = models.CharField(max_length=16, blank=True, default="")

class MatchParticipant(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name="participants")
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name="matches")

    team = models.CharField(max_length=16, blank=True, default="")  # Blue/Red, etc.
    agent = models.ForeignKey(Agent, null=True, blank=True, on_delete=models.SET_NULL)

    kills = models.IntegerField(default=0)
    deaths = models.IntegerField(default=0)
    assists = models.IntegerField(default=0)
    acs = models.IntegerField(default=0)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["match", "player"], name="uq_match_player")
        ]
