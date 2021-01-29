import requests
from datetime import datetime
from .User import User
from .Map import Map
from .Score import Score
from .Utils import Mode, Mods


class OsuClient:
    def __init__(self, key):
        self.api_key = key

    def get_user(self, user_id: int, mode: Mode = Mode.STANDARD) -> User:
        params = {"k": self.api_key, "u": user_id, "m": mode.value}
        return self.fetch_user(params)

    def get_user_from_name(self, username: str, mode: Mode = Mode.STANDARD) -> User:
        params = {"k": self.api_key, "u": username, "type": "string", "m": mode.value}
        return self.fetch_user(params)

    def fetch_user(self, params):
        r = requests.get("https://osu.ppy.sh/api/get_user", params=params)
        user_json = r.json()
        if user_json:
            user = User(user_json[0], self)
            return user

    def get_scores(self, map_id: int, username: str = None, user_id: int = None,
                   mode: Mode = Mode.STANDARD, mods: Mods = None, limit: int = 50):
        params = {"k": self.api_key, "b": map_id, "m": mode.value}
        if username:
            params['u'] = username
            params['type'] = "string"
        elif user_id:
            params['u'] = user_id
            params['type'] = "id"
        if mods:
            params['mods'] = mods.value
        if 1 <= limit <= 100:
            params['limit'] = limit

        return self.fetch_scores(params)

    def fetch_scores(self, params):
        r = requests.get("https://osu.ppy.sh/api/get_scores", params=params)
        scores_json = r.json()
        if scores_json:
            return [Score(score_info, self, params['b']) for score_info in scores_json]

    def get_map(self, map_id: int) -> Map:
        params = {"k": self.api_key, "b": map_id}
        return self.fetch_maps(params)[0]

    # todo: add error handling if invalid mods given
    def get_maps(self, set_id: int = None, map_id: int = None, username: str = None, user_id: int = None,
                 map_hash: str = None, mode: Mode = Mode.STANDARD, converts: int = 0,
                 limit: int = 500, mods: Mods = Mods.NM, since: datetime = None):
        params = {"k": self.api_key, 'm': mode.value, 'mods': mods.value}
        if set_id:
            params['s'] = set_id
        if map_id:
            params['b'] = map_id
        if username:
            params['u'] = username
            params['type'] = "string"
        elif user_id:
            params['u'] = user_id
            params['type'] = "id"
        if map_hash:
            params['h'] = map_hash
        if converts == 1:
            params['a'] = 1
        if 0 <= limit <= 500:
            params['limit'] = limit
        if since:
            params['since'] = since.strftime("%Y-%m-%d %H:%M:%S")

        return self.fetch_maps(params)

    def fetch_maps(self, params) -> [Map]:
        r = requests.get("https://osu.ppy.sh/api/get_beatmaps", params=params)
        maps_json = r.json()
        if maps_json:
            return [Map(map_info, self) for map_info in maps_json]
