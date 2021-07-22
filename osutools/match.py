from datetime import datetime
from .utils import *
from .score import MultiScore


class Match:
    """A past/ongoing multiplayer lobby

    Attributes:
        client: OsuClient that created the instance
        match_id: id of the lobby
        name: the title of the lobby
        start_time: timestamp of when the match started
        end_time: timestamp of when the match ended (or None if it is ongoing)
        games: [Game] list of game objects containing info on each specific round of the lobby
        url: the url for the match to view in a browser
    """

    def __init__(self, match_info, client):
        match_attr = match_info["match"]
        games_list = match_info["games"]
        self.client = client
        self.match_id = int(match_attr["match_id"])
        self.name = match_attr["name"]
        self.start_time = datetime.strptime(
            match_attr["start_time"], "%Y-%m-%d %H:%M:%S"
        )
        self.end_time = (
            datetime.strptime(match_attr["end_time"], "%Y-%m-%d %H:%M:%S")
            if match_attr["end_time"]
            else None
        )
        self.games = [
            Game(game_info, client, self.match_id) for game_info in games_list
        ]
        self.url = f"https://osu.ppy.sh/community/matches/{self.match_id}"

    def __repr__(self):
        games = "\n".join([str(x) for x in self.games])
        return f"{self.match_id}: {self.name}\n{games}"


class Game:
    """A specific round of a multiplayer lobby

    Attributes:
        game_id: the id of the round
        match_id: the id of the lobby it happened in
        client: OsuClient that created the instance
        start_time: timestamp of when the game started
        end_time: timestamp of when the game ended
        play_mode: the gamemode the game happened in
        map_id: the id of the map that was played
        match_type: doesn't seem to actually do anything? but the api returns it so I'm capturing it
        score_type: enum representing how the game was scored
        team_type: enum representing how the teams were set
        mods: enum representing the mods that were used
        scores: a list of multiplayer-specific score objects representing the results of the round for each player
    """

    def __init__(self, game_info, client, match_id: int):
        self.game_id = int(game_info["game_id"])
        self.match_id = match_id
        self.client = client
        self.start_time = datetime.strptime(
            game_info["start_time"], "%Y-%m-%d %H:%M:%S"
        )
        self.end_time = datetime.strptime(game_info["end_time"], "%Y-%m-%d %H:%M:%S")
        self.play_mode = Mode(int(game_info["play_mode"]))
        self.map_id = int(game_info["beatmap_id"])
        self.match_type = int(game_info["match_type"])
        self.score_type = WinCon(int(game_info["scoring_type"]))
        self.team_type = TeamType(int(game_info["team_type"]))
        self.mods = Mods(int(game_info["mods"]))
        self.scores = [
            MultiScore(
                score_info, client, self.map_id, match_id, self.game_id, self.mods
            )
            for score_info in game_info["scores"]
        ]

    def get_players(self):
        """The users who took part in this game. Not an api call.

        Returns:
            [int]: list of user id's
        """
        return [score.user_id for score in self.scores]

    def __repr__(self):
        return f"{self.game_id}: {self.score_type.name} {self.team_type.name} game with {self.mods} on map {self.map_id}"
