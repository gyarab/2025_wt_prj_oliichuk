from app.models import Player


def upsert_player(profile: dict) -> tuple[Player, bool]:
    """Upsert a Player from a profile payload.

    Accepts either the shape produced by the JS client (with `raw: { account, mmr }`)
    or a flattened shape (`raw_account`, `mmr`). Returns (player, created).
    """
    puuid = profile.get("puuid")
    if not puuid:
        raise ValueError("profile missing 'puuid'")

    # Riot id can be either 'name#tag' or separate fields
    riot_id = profile.get("riot_id") or f"{profile.get('game_name','')}#{profile.get('tag_line','')}"
    riot_name, riot_tag = ("", "")
    if riot_id and "#" in riot_id:
        riot_name, riot_tag = riot_id.split("#", 1)

    # Support both nested and flat payload shapes
    account_raw = profile.get("raw", {}).get("account") or profile.get("raw_account") or profile.get("account_raw")
    mmr_raw = profile.get("raw", {}).get("mmr") or profile.get("mmr") or profile.get("mmr_raw")

    player, created = Player.objects.update_or_create(
        puuid=puuid,
        defaults={
            "game_name": riot_name,
            "tag_line": riot_tag,
            "region": profile.get("region", ""),
            "account_level": profile.get("account_level"),
            "account_raw": account_raw,
            "mmr_raw": mmr_raw,
        },
    )
    return player, created