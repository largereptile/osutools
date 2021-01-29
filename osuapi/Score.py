from datetime import datetime
from .Utils import *


class Score:
    def __init__(self, score_info, client, map_id):
        self.client = client
        self.map_id = map_id
        self.score_id = int(score_info['score_id'])
        self.score = int(score_info['score'])
        self.username = score_info['username']
        self.user_id = score_info['user_id']
        self.timestamp = datetime.strptime(score_info['date'], "%Y-%m-%d %H:%M:%S")
        self.num_300 = int(score_info['count300'])
        self.num_100 = int(score_info['count100'])
        self.num_50 = int(score_info['count50'])
        self.misses = int(score_info['countmiss'])
        self.max_combo = int(score_info['maxcombo'])
        self.num_katu = int(score_info['countkatu'])
        self.num_geki = int(score_info['countgeki'])
        self.perfect = score_info['perfect'] == "1"
        self.mods = Mods(int(score_info['enabled_mods']))
        self.rank = score_info['rank']
        self.pp = float(score_info['pp'])
        self.replay_available = score_info['replay_available'] == "1"

    def __repr__(self):
        return f"{self.mods} score on beatmap {self.map_id} by {self.username}"
