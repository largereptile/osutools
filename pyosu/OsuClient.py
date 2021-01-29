import requests
from datetime import datetime
from .User import User
from .Map import Map
from .Score import Score
from .Utils import *


def _id_or_name(params, username, user_id):
    if username:
        params['u'] = username
        params['type'] = "string"
    elif user_id:
        params['u'] = user_id
        params['type'] = "id"


class OsuClient:
    def __init__(self, key):
        self.api_key = key

    def _request_api(self, url: str, params: dict):
        params['k'] = self.api_key
        r = requests.get(f"https://osu.ppy.sh/api/{url}", params=params)
        return r.json() if r.json() else None

    def fetch_user(self, user_id: int = None, username: str = None, mode: Mode = Mode.STANDARD):
        if not (username or user_id):
            return
        params = {"m": mode.value}
        _id_or_name(params, username, user_id)
        user_json = self._request_api("get_user", params)
        if user_json:
            return User(user_json[0], self)

    def fetch_scores(self, map_id: int, username: str = None, user_id: int = None,
                     mode: Mode = Mode.STANDARD, mods: Mods = None, limit: int = 50):
        params = {"b": map_id, "m": mode.value}
        _id_or_name(params, username, user_id)
        if mods:
            params['mods'] = mods.value
        if 1 <= limit <= 100:
            params['limit'] = limit

        scores_json = self._request_api("get_scores", params)
        if scores_json:
            return [Score(score_info, self, params['b']) for score_info in scores_json]

    def fetch_map(self, map_id: int):
        return self.fetch_maps(map_id=map_id)[0]

    # todo: add error handling if invalid mods given
    def fetch_maps(self, set_id: int = None, map_id: int = None, username: str = None, user_id: int = None,
                   map_hash: str = None, mode: Mode = Mode.STANDARD, converts: int = 0,
                   limit: int = 500, mods: Mods = Mods.NM, since: datetime = None):
        params = {"m": mode.value, "mods": mods.value}
        _id_or_name(params, username, user_id)
        if set_id:
            params['s'] = set_id
        if map_id:
            params['b'] = map_id
        if map_hash:
            params['h'] = map_hash
        if converts == 1:
            params['a'] = 1
        if 0 <= limit <= 500:
            params['limit'] = limit
        if since:
            params['since'] = since.strftime("%Y-%m-%d %H:%M:%S")

        maps_json = self._request_api("get_beatmaps", params)
        if maps_json:
            return [Map(map_info, self) for map_info in maps_json]

    def fetch_user_best(self, username: str = None, user_id: int = None, mode: Mode = Mode.STANDARD, limit: int = 10):
        if not (username or user_id):
            return
        params = {"k": self.api_key, "m": mode.value, "limit": limit}
        _id_or_name(params, username, user_id)

        best_json = self._request_api("get_user_best", params)
        if best_json:
            return [Score(score_info, self, score_info['beatmap_id']) for score_info in best_json]
