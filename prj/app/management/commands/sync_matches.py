from django.core.management.base import BaseCommand
from django.conf import settings
from django.utils import timezone

from app.models import RiotAccount, Match
from app.val_client import ValClient
from app.sync_val import persist_match


class Command(BaseCommand):
    help = "Sync VAL matches from VAL-MATCH-V1 endpoints."

    def add_arguments(self, parser):
        parser.add_argument("--puuid", required=False)
        parser.add_argument("--limit", type=int, default=20)

    def handle(self, *args, **opts):
        base_url = getattr(settings, "VAL_API_BASE_URL", "")
        api_key = getattr(settings, "VAL_API_KEY", "")
        auth_mode = getattr(settings, "VAL_API_AUTH_MODE", "x-riot-token")

        if not base_url or not api_key:
            raise SystemExit(
                "Missing settings VAL_API_BASE_URL / VAL_API_KEY. "
                "Set env vars or put them into settings.py."
            )

        client = ValClient(base_url=base_url, api_key=api_key, auth_mode=auth_mode)

        accounts = RiotAccount.objects.all()
        if opts.get("puuid"):
            accounts = accounts.filter(puuid=opts["puuid"])

        if not accounts.exists():
            self.stdout.write(self.style.WARNING(
                "No RiotAccount found. Create one in /admin first (user + puuid + region)."
            ))
            return

        for acc in accounts:
            self.stdout.write(f"Syncing puuid={acc.puuid} region={acc.region}")

            matchlist = client.matchlist_by_puuid(acc.puuid)
            history = matchlist.get("history") or matchlist.get("History") or []
            history = history[: opts["limit"]]

            imported = 0
            skipped = 0

            for item in history:
                match_id = item.get("matchId") or item.get("matchID") or item.get("MatchID")
                if not match_id:
                    continue

                if Match.objects.filter(riot_match_id=str(match_id)).exists():
                    skipped += 1
                    continue

                match_json = client.match_by_id(str(match_id))
                persist_match(match_json)
                imported += 1

            acc.last_synced_at = timezone.now()
            acc.save(update_fields=["last_synced_at"])

            self.stdout.write(self.style.SUCCESS(f"Imported={imported}, skipped(existing)={skipped}"))