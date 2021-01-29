import requests
from .User import User
from .Utils import Mode


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

    def get_scores(self):
        pass

    def get_map(self, map_id: int):
        params = {"k": self.api_key, }

    def get_maps(self):
        pass

    def search_maps(self):
        pass