from django.db import models

class Player(models.Model):
    puuid = models.CharField(max_length=128, unique=True)
    game_name = models.CharField(max_length=64, blank=True, default="")
    tag_line = models.CharField(max_length=16, blank=True, default="")


class Match(models.Model):
    riot_match_id = models.CharField(max_length=64, unique=True)
    started_at = models.DateTimeField(blank=True, null=True)
    game_version = models.CharField(max_length=64, blank=True, default="")
    queue_id = models.CharField(max_length=32, blank=True, default="")
    

class MatchStats(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name="stats")
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name="match_stats")
    team = models.CharField(max_length=16, blank=True, default="")
    kills = models.IntegerField(default=0)
    deaths = models.IntegerField(default=0)
    assists = models.IntegerField(default=0)
    acs = models.IntegerField(default=0)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=("match", "player"), name="uq_match_player"),
        ]
