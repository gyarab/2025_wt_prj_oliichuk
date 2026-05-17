import time
import requests

class ValClient:
    def __init__(self, base_url: str, api_key: str, auth_mode: str = "x-riot-token", timeout: int = 20):
        self.base_url = base_url.rstrip("/")
        self.api_key = (api_key or "").strip()
        self.auth_mode = (auth_mode or "x-riot-token").strip().lower()
        self.timeout = timeout

        if not self.api_key:
            raise RuntimeError("RIOT API key is missing/empty (ValClient.api_key).")        

    def _headers(self):
        if self.auth_mode in {"x-riot-token", "x_riot_token", "riot-token", "riot"}:
            return {"X-Riot-Token": self.api_key}
        # fallback, only if you ever need it for something else
        return {"Authorization": f"Bearer {self.api_key}"}

    def get(self, path: str, params=None, retries: int = 3):
        url = f"{self.base_url}{path}"
        for attempt in range(retries):
            r = requests.get(url, headers=self._headers(), params=params, timeout=self.timeout)
            if r.status_code == 429:
                wait = 1 + attempt * 2
                time.sleep(wait)
                continue
            r.raise_for_status()
            return r.json()
        raise RuntimeError("Rate limited too many times (429).")

    def matchlist_by_puuid(self, puuid: str):
        return self.get(f"/val/match/v1/matchlists/by-puuid/{puuid}")

    def match_by_id(self, match_id: str):
        return self.get(f"/val/match/v1/matches/{match_id}")
