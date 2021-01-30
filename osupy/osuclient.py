import requests
from datetime import datetime
from .user import User
from .map import Map
from .score import Score, RecentScore
from .utils import *
from .match import Match


class OsuClient:
    """Client object for interacting with the osu! api.

    Attributes:
        api_key (str): the api key for your osu! application

    """
    def __init__(self, key: str):
        """Initialise the client with an api key.

        Args:
            key: The api key for your osu! application.
        """
        self.api_key = key

    @staticmethod
    def _id_or_name(params: dict, username: str, user_id: int):
        """Configured a given parameter dict depending on if it has received a valid username or user_id.

        Args:
            params: dict of parameters to be sent
            username: username or None if given a user_id
            user_id: user id or None if given a username

        Returns:
            None
        """
        if username:
            params['u'] = username
            params['type'] = "string"
        elif user_id:
            params['u'] = user_id
            params['type'] = "id"

    def _request_api(self, url: str, params: dict):
        """Private method to generalise api requests.

        Args:
            url: the api endpoint to request to (e.g. "get_user")
            params: dict of prepared parameters for the endpoint you are attempting to request

        Returns:
            dict: results of the api request (or None if unsuccessful)
        """
        params['k'] = self.api_key
        r = requests.get(f"https://osu.ppy.sh/api/{url}", params=params)
        return r.json() if r.json() else None

    def fetch_user(self, user_id: int = None, username: str = None, mode: Mode = Mode.STANDARD):
        """Make an api request to get information about a given user.

        Args:
            user_id: id of the user
            username: name of the user
            mode: enum representing the osu! gamemode you want the information for

        Returns:
            osupy.User: User object representing the requested user
        """
        if not (username or user_id):
            return
        params = {"m": mode.value}
        self._id_or_name(params, username, user_id)
        user_json = self._request_api("get_user", params)
        if user_json:
            return User(user_json[0], self)

    def fetch_scores(self, map_id: int, username: str = None, user_id: int = None,
                     mode: Mode = Mode.STANDARD, mods: Mods = None, limit: int = 50):
        """Make an api request to retrieve information about scores on a given beatmap.

        Args:
            map_id: the id of the beatmap to retrieve scores for
            username: username of a player to filter by
            user_id: id of a player to filter by
            mode: enum representing the osu! gamemode you want information for
            mods: enum representing the mod combination to filter by
            limit: number of scores to retrieve (max 100)

        Returns:
            [Score]: List of Score objects containing information about a given score
        """
        params = {"b": map_id, "m": mode.value}
        self._id_or_name(params, username, user_id)
        if mods:
            params['mods'] = mods.value
        if 1 <= limit <= 100:
            params['limit'] = limit

        scores_json = self._request_api("get_scores", params)
        if scores_json:
            return [Score(score_info, self, params['b']) for score_info in scores_json]

    def fetch_map(self, map_id: int):
        """Wrapper for the api call of selecting a map from an id and taking the first one, as it would only return one map anyway.

        Args:
            map_id: the map to get information for

        Returns:
            Map: Map object containing information about the map requested
        """
        return self.fetch_maps(map_id=map_id)[0]

    # todo: add error handling if invalid mods given
    def fetch_maps(self, set_id: int = None, map_id: int = None, username: str = None, user_id: int = None,
                   map_hash: str = None, mode: Mode = Mode.STANDARD, converts: bool = False,
                   limit: int = 500, mods: Mods = Mods.NM, since: datetime = None):
        """Api call to search osu!'s beatmap pool.

        Args:
            set_id: the id of a beatmapset to filter by
            map_id: the id of a specific map to return
            username: filter by mapper's username
            user_id: filter by mapper's id
            map_hash: the md5 hash of a beatmap
            mode: enum representing the osu! gamemode to filter by
            converts: whether to include converted maps for a gamemode
            limit: number of maps to return (max and default 500)
            mods: enum representing the mod combination to filter by
            since: limit beatmaps found to between this date and the present

        Returns:
            [Map]: List of Map objects containing information about the maps requested
        """
        params = {"m": mode.value, "mods": mods.value}
        self._id_or_name(params, username, user_id)
        if set_id:
            params['s'] = set_id
        if map_id:
            params['b'] = map_id
        if map_hash:
            params['h'] = map_hash
        if converts:
            params['a'] = 1
        if 0 <= limit <= 500:
            params['limit'] = limit
        if since:
            params['since'] = since.strftime("%Y-%m-%d %H:%M:%S")

        maps_json = self._request_api("get_beatmaps", params)
        if maps_json:
            return [Map(map_info, self) for map_info in maps_json]

    def fetch_user_best(self, username: str = None, user_id: int = None, mode: Mode = Mode.STANDARD, limit: int = 10):
        """Api request to find a users best scores.

        Args:
            username: username of user
            user_id: id of a user
            mode: enum representing mode to get the top plays from
            limit: number of best scores to retrieve (max 100)

        Returns:
            [Score]: List of Score objects representing the user's best plays
        """
        if not (username or user_id):
            return
        params = {"m": mode.value}
        if 1 <= limit <= 100:
            params['limit'] = limit
        self._id_or_name(params, username, user_id)

        best_json = self._request_api("get_user_best", params)
        if best_json:
            return [Score(score_info, self, score_info['beatmap_id']) for score_info in best_json]

    def fetch_user_recent(self, username: str = None, user_id: int = None, mode: Mode = Mode.STANDARD, limit: int = 10):
        """Api request to retrieve a user's recent scores (within the last 24 hours).

        Args:
            username: username of user
            user_id: id of user
            mode: enum representing osu! gamemode to retrieve scores for
            limit: number of scores to retrieve (max 100)

        Returns:
            [Score]: List of Score objects representing a user's recent plays
        """
        if not (username or user_id):
            return
        params = {"m": mode.value}
        self._id_or_name(params, username, user_id)
        if 1 <= limit <= 100:
            params['limit'] = limit
        recent_json = self._request_api("get_user_recent", params)
        if recent_json:
            return [RecentScore(score_info, self, score_info['beatmap_id']) for score_info in recent_json]

    """
    Requesting via beatmap and user was broken when I was testing but I'll leave the function here in case it's just
    me being dumb
    def fetch_replay(self,  score_id: int = None, username: str = None, user_id: int = None,
                     mode: Mode = Mode.STANDARD, map_id: int = None, mods: Mods = Mods.NM):
        params = {}
        if score_id:
            params['s'] = score_id
        else:
            if not (username or user_id) or not map_id:
                return
            _id_or_name(params, username, user_id)
            params['b'] = map_id
            params['m'] = mode.value
            params['mods'] = mods.value
        return self._request_api("get_replay", params)
    
    """

    def fetch_replay(self, score_id: int):
        """Api request to fetch a replay for a given score

        Args:
            score_id: score to retrieve replay for

        Returns:
            str: base64 representation of LZMA stream, not .osr file. See https://osu.ppy.sh/help/wiki/osu!_File_Formats/Osr_(file_format) for details
        """
        replay_json = self._request_api("get_replay", {"s": score_id})
        return replay_json["content"] if "content" in replay_json else None

    def fetch_match(self, match_id: int):
        """Api request to fetch details about a given multiplayer lobby, past or ongoing

        Args:
            match_id: id of the match

        Returns:
            Match: Match object representing all the information available about the match requested.
        """
        match_json = self._request_api("get_match", {"mp": match_id})
        return Match(match_json, self)
