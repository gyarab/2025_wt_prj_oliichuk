from django.shortcuts import render

#nas kontroler
def render_about(request): 
    return render(request, 'home.html')

def render_api_playground(request):
    return render(request, 'api_playground.html')

#django endpoint 

import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .models import Player
from .services.upsert import upsert_player as service_upsert_player

@csrf_exempt  # OK for local dev; for prod use a token or auth (see note below)
@require_POST
def upsert_player(request):
    payload = json.loads(request.body.decode("utf-8"))

    # expecting the shape from your JS: { puuid, region, account_level, raw: { account, mmr }, riot_id }
    try:
        player, created = service_upsert_player(payload)
    except Exception as exc:
        return JsonResponse({"ok": False, "error": str(exc)}, status=400)

    return JsonResponse({"ok": True, "created": created, "player_id": player.id, "puuid": player.puuid})
