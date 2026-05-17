import json
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError

from app.sync_val import persist_match


class Command(BaseCommand):
    help = "Import a VAL match JSON file into Match, Player, and MatchStats."

    def add_arguments(self, parser):
        parser.add_argument("file", help="Path to a JSON file containing one match payload")

    def handle(self, *args, **opts):
        file_path = Path(opts["file"])
        if not file_path.exists():
            raise CommandError(f"File does not exist: {file_path}")

        try:
            match_json = json.loads(file_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise CommandError(f"Invalid JSON in {file_path}: {exc}") from exc

        match_obj = persist_match(match_json)
        self.stdout.write(self.style.SUCCESS(f"Imported match {match_obj.riot_match_id}"))