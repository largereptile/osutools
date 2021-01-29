from datetime import datetime
from .Utils import *


class BaseScore:
    def __init__(self, score_info, client, map_id):
        self.client = client
        self.map_id = map_id
        self.num_300 = int(score_info['count300'])
        self.num_100 = int(score_info['count100'])
        self.num_50 = int(score_info['count50'])
        self.misses = int(score_info['countmiss'])
        self.max_combo = int(score_info['maxcombo'])
        self.num_katu = int(score_info['countkatu'])
        self.num_geki = int(score_info['countgeki'])
        self.perfect = score_info['perfect'] == "1"
        self.user_id = int(score_info['user_id'])
        self.score = int(score_info['score'])
        self.username = score_info['username'] if "username" in score_info else self.user_id


class Score(BaseScore):
    def __init__(self, score_info, client, map_id):
        self.score_id = int(score_info['score_id'])
        self.timestamp = datetime.strptime(score_info['date'], "%Y-%m-%d %H:%M:%S")
        self.mods = Mods(int(score_info['enabled_mods']))
        self.rank = score_info['rank']
        self.pp = float(score_info['pp'])
        self.replay_available = score_info['replay_available'] == "1"
        super().__init__(score_info, client, map_id)

    def __repr__(self):
        return f"{self.mods} score on beatmap {self.map_id} by {self.username}"


class RecentScore(BaseScore):
    def __init__(self, score_info, client, map_id):
        self.timestamp = datetime.strptime(score_info['date'], "%Y-%m-%d %H:%M:%S")
        self.mods = Mods(int(score_info['enabled_mods']))
        self.rank = score_info['rank']
        super().__init__(score_info, client, map_id)

    def __repr__(self):
        return f"{self.mods} score on beatmap {self.map_id} by {self.username}"


class MultiScore(BaseScore):
    def __init__(self, score_info: dict, client, map_id: int, match_id: int, game_id: int, mods: Mods):
        self.game_id = game_id
        self.match_id = match_id
        self.slot = int(score_info["slot"])
        self.team = Teams(int(score_info["team"]))
        self.score = int(score_info["score"])
        self.rank = int(score_info["rank"])  # says not used on the wiki but lists it anyway so ill catch it just in case
        self.passed = score_info["pass"] == "1"
        self.mods = mods if not score_info["enabled_mods"] else Mods(mods.value + int(score_info["enabled_mods"]))
        super().__init__(score_info, client, map_id)

    def __repr__(self):
        return f"{self.mods} score on beatmap {self.map_id} by {self.user_id} in match {self.match_id}"
