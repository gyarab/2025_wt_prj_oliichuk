from django.db import transaction
from django.utils.dateparse import parse_datetime

from .models import Match, MatchStats, Player


def _get(dct, *keys, default=None):
    for path in keys:
        cur = dct
        ok = True
        for k in path:
            if not isinstance(cur, dict) or k not in cur:
                ok = False
                break
            cur = cur[k]
        if ok:
            return cur
    return default


@transaction.atomic
def persist_match(match_json: dict):
    match_id = _get(match_json, ("matchInfo", "matchId"), ("matchId",), default=None)
    if not match_id:
        raise ValueError("Missing matchId in match payload")

    started_raw = _get(match_json, ("matchInfo", "gameStartTime"), ("matchInfo", "startedAt"), default=None)
    started_at = parse_datetime(started_raw) if isinstance(started_raw, str) else None

    match_obj, created = Match.objects.get_or_create(
        riot_match_id=str(match_id),
        defaults={"started_at": started_at},
    )
    if not created and match_obj.started_at is None and started_at:
        match_obj.started_at = started_at
        match_obj.save(update_fields=["started_at"])

    players = match_json.get("players") or match_json.get("Players") or []
    for p in players:
        puuid = p.get("puuid")
        if not puuid:
            continue

        player_obj, _ = Player.objects.get_or_create(
            puuid=str(puuid),
            defaults={
                "game_name": str(p.get("gameName") or ""),
                "tag_line": str(p.get("tagLine") or ""),
            },
        )

        gn = p.get("gameName")
        tl = p.get("tagLine")
        if (gn and player_obj.game_name != gn) or (tl and player_obj.tag_line != tl):
            if gn:
                player_obj.game_name = str(gn)
            if tl:
                player_obj.tag_line = str(tl)
            player_obj.save(update_fields=["game_name", "tag_line"])

        stats = p.get("stats") or {}
        kills = stats.get("kills", p.get("kills", 0)) or 0
        deaths = stats.get("deaths", p.get("deaths", 0)) or 0
        assists = stats.get("assists", p.get("assists", 0)) or 0
        acs = stats.get("acs", stats.get("score", p.get("acs", 0))) or 0

        MatchStats.objects.update_or_create(
            match=match_obj,
            player=player_obj,
            defaults={
                "team": str(p.get("teamId") or p.get("team") or ""),
                "kills": int(kills),
                "deaths": int(deaths),
                "assists": int(assists),
                "acs": int(acs),
            },
        )

    return match_obj
