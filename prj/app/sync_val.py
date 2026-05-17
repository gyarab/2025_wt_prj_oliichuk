from django.db import transaction
from django.utils.dateparse import parse_datetime

from .models import Match, Player, MatchParticipant, Map, Agent

def _get(dct, *keys, default=None):
    """Try multiple nested key paths.
    Example: _get(data, ("matchInfo","matchId"), ("matchId",), default=None)
    """
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

def upsert_map(match_json):
    map_id = _get(match_json, ("matchInfo","mapId"), ("matchInfo","map"), default="")
    map_name = _get(match_json, ("matchInfo","map"), default="") or str(map_id)
    if not map_id and not map_name:
        return None
    obj, _ = Map.objects.get_or_create(
        riot_map_id=str(map_id),
        defaults={"name": str(map_name)},
    )
    if map_name and obj.name != map_name:
        obj.name = str(map_name)
        obj.save(update_fields=["name"])
    return obj

def upsert_agent(p):
    agent_id = p.get("characterId") or p.get("agentId") or ""
    agent_name = p.get("agentName") or ""
    if not agent_id and not agent_name:
        return None
    obj, _ = Agent.objects.get_or_create(
        riot_agent_id=str(agent_id or agent_name),
        defaults={"name": str(agent_name or agent_id)},
    )
    if agent_name and obj.name != agent_name:
        obj.name = str(agent_name)
        obj.save(update_fields=["name"])
    return obj

@transaction.atomic
def persist_match(match_json: dict):
    # match id
    match_id = _get(match_json, ("matchInfo","matchId"), ("matchId",), default=None)
    if not match_id:
        raise ValueError("Missing matchId in match payload")

    # time (might be ISO string or epoch ms - adjust when you see real JSON)
    started_raw = _get(match_json, ("matchInfo","gameStartTime"), ("matchInfo","startedAt"), default=None)
    started_at = None
    if isinstance(started_raw, str):
        started_at = parse_datetime(started_raw)

    map_obj = upsert_map(match_json)

    match_obj, created = Match.objects.get_or_create(
        riot_match_id=str(match_id),
        defaults={"started_at": started_at, "map": map_obj},
    )
    if not created:
        dirty = False
        if match_obj.started_at is None and started_at:
            match_obj.started_at = started_at
            dirty = True
        if match_obj.map_id is None and map_obj:
            match_obj.map = map_obj
            dirty = True
        if dirty:
            match_obj.save()

    # players array key differs by provider; try both common options
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
            }
        )

        # optionally keep names updated
        gn = p.get("gameName")
        tl = p.get("tagLine")
        if (gn and player_obj.game_name != gn) or (tl and player_obj.tag_line != tl):
            if gn:
                player_obj.game_name = str(gn)
            if tl:
                player_obj.tag_line = str(tl)
            player_obj.save(update_fields=["game_name", "tag_line"])

        agent_obj = upsert_agent(p)

        stats = p.get("stats") or {}
        kills = stats.get("kills", p.get("kills", 0)) or 0
        deaths = stats.get("deaths", p.get("deaths", 0)) or 0
        assists = stats.get("assists", p.get("assists", 0)) or 0

        # ACS key differs; will adjust after you paste real JSON
        acs = stats.get("acs", stats.get("score", p.get("acs", 0))) or 0

        MatchParticipant.objects.update_or_create(
            match=match_obj,
            player=player_obj,
            defaults={
                "team": str(p.get("teamId") or p.get("team") or ""),
                "agent": agent_obj,
                "kills": int(kills),
                "deaths": int(deaths),
                "assists": int(assists),
                "acs": int(acs),
            }
        )

    return match_obj