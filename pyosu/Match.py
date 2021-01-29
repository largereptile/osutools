from datetime import datetime
from .Utils import *
from .Score import MultiScore


class Match:
    def __init__(self, match_info, client):
        match_attr = match_info['match']
        games_list = match_info['games']
        self.client = client
        self.match_id = int(match_attr['match_id'])
        self.name = match_attr['name']
        self.start_time = datetime.strptime(match_attr['start_time'], "%Y-%m-%d %H:%M:%S")
        self.end_time = datetime.strptime(match_attr['end_time'], "%Y-%m-%d %H:%M:%S") if match_attr["end_time"] else None
        self.games = [Game(game_info, client, self.match_id) for game_info in games_list]
        self.url = f"https://osu.ppy.sh/community/matches/{self.match_id}"

    def __repr__(self):
        games = "\n".join([str(x) for x in self.games])
        return f"{self.match_id}: {self.name}\n{games}"


class Game:
    def __init__(self, game_info, client, match_id: int):
        self.game_id = int(game_info['game_id'])
        self.match_id = match_id
        self.client = client
        self.start_time = datetime.strptime(game_info['start_time'], "%Y-%m-%d %H:%M:%S")
        self.end_time = datetime.strptime(game_info['end_time'], "%Y-%m-%d %H:%M:%S")
        self.play_mode = Mode(int(game_info['play_mode']))
        self.map_id = int(game_info['beatmap_id'])
        self.match_type = int(game_info['match_type'])
        self.score_type = WinCon(int(game_info['scoring_type']))
        self.team_type = TeamType(int(game_info['team_type']))
        self.mods = Mods(int(game_info['mods']))
        self.scores = [MultiScore(score_info, client, self.map_id, match_id, self.game_id, self.mods)
                       for score_info in game_info['scores']]

    def __repr__(self):
        return f"{self.game_id}: {self.score_type.name} {self.team_type.name} game with {self.mods} on map {self.map_id}"
