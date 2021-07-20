from .utils import *


class BaseScore:
    """Base class for a score, all types of score share these attributes.

    Attributes:
        client: OsuClient that created this object instance
        map_id: the map the score is for
        num_300: the number of 300s hit in the score
        num_100: the number of 100s hit in the score
        num_50: the number of 50s hit in the score
        misses: the number of misses in the score
        max_combo: the highest combo reached by the player in this score
        num_katu: the number of katu hit
        num_geki: the number of geki hit
        perfect: boolean representing if the maximum combo for the map was reached
        user_id: id of the player who set the score
        score: the actual numerical score for the play
        username: name of the player who set the score
        successful_hits: number of non-misses
        map_total_hits: maximum number of non-misses
        accuracy_dec: the player's accuracy as a decimal
    """

    def __init__(self, score_info, client):
        self.client = client
        self.num_300 = int(score_info['count300'])
        self.num_100 = int(score_info['count100'])
        self.num_50 = int(score_info['count50'])
        self.misses = int(score_info['countmiss'])
        self.max_combo = int(score_info['maxcombo'])
        self.num_katu = int(score_info['countkatu'])
        self.num_geki = int(score_info['countgeki'])
        self.perfect = (score_info['perfect'] == "1") or score_info['perfect']
        self.user_id = int(score_info['user_id']) if "user_id" in score_info else None
        self.score = int(score_info['score'])
        self.username = score_info['username'] if "username" in score_info else self.user_id
        self.successful_hits = self.num_50 + self.num_100 + self.num_300
        self.map_total_hits = self.successful_hits + self.misses
        temp_accuracy = (self.num_50 * 50 + self.num_100 * 100 + self.num_300 * 300) / (
                self.map_total_hits * 300) if self.map_total_hits != 0 else 0
        self.accuracy_dec = min(1.0, max(0.0, temp_accuracy))

    def fetch_user(self):
        """Make an api call to get more information about user.

        Returns:
            User: the user who set the score
        """
        return self.client.fetch_user(user_id=self.user_id)


class Score(BaseScore):
    """Generic score object, returned when searching or getting best plays.

    Attributes:
        score_id: the id of the score
        timestamp: when the score was set
        mods: enum representing the mod combination used
        rank: letter representing how good the score is
        pp: the amount of pp rewarded for the score
        replay_available: boolean representing if it is possible to download the replay of the map

    """

    def __init__(self, score_info, client, map_id):
        self.map_id = map_id
        self.score_id = int(score_info['score_id'])
        self.timestamp = datetime.strptime(score_info['date'], "%Y-%m-%d %H:%M:%S")
        self.mods = Mods(int(score_info['enabled_mods']))
        self.rank = score_info['rank']
        self.pp = float(score_info['pp']) if score_info['pp'] else 0
        self.replay_available = score_info['replay_available'] == "1"
        super().__init__(score_info, client)

    def fetch_map(self):
        return self.client.fetch_map(map_id=self.map_id)

    def __repr__(self):
        return f"{self.mods} score on beatmap {self.map_id} by {self.username}"


class RecentScore(BaseScore):
    """Score object used when getting recent scores.

    Attributes:
        timestamp: when the score was set
        mods: the mod combination used
        rank: letter representing how good the score is
    """

    def __init__(self, score_info, client, map_id):
        self.map_id = map_id
        self.timestamp = datetime.strptime(score_info['date'], "%Y-%m-%d %H:%M:%S")
        self.mods = Mods(int(score_info['enabled_mods']))
        self.rank = score_info['rank']
        super().__init__(score_info, client)

    def __repr__(self):
        return f"{self.mods} score on beatmap {self.map_id} by {self.username}"


class MultiScore(BaseScore):
    """Multiplayer lobby score object.

    Attributes:
        game_id: the game it was set in
        match_id: the match it ws set in
        slot: where in the lobby the player was positioned
        team: what team the player was on
        rank: letter achieved
        passed: boolean representing if the player passed or not
        mods: all the mods this player used, not necessarily the same as other scores from the same game

    """

    def __init__(self, score_info: dict, client, map_id: int, match_id: int, game_id: int, mods: Mods):
        self.map_id = map_id
        self.game_id = game_id
        self.match_id = match_id
        self.slot = int(score_info["slot"])
        self.team = Teams(int(score_info["team"]))
        self.rank = int(
            score_info["rank"])  # says not used on the wiki but lists it anyway so ill catch it just in case
        self.passed = score_info["pass"] == "1"
        self.mods = mods if not score_info["enabled_mods"] else Mods(mods.value + int(score_info["enabled_mods"]))
        super().__init__(score_info, client)

    def __repr__(self):
        return f"{self.mods} score on beatmap {self.map_id} by {self.user_id} in match {self.match_id}"


class LocalScore(BaseScore):
    def __init__(self, score_info, client, replay_hash):
        super().__init__(score_info, client)
        self.map_hash = score_info["map_hash"]
        self.map = self.client.get_local_map(self.map_hash)
        self.md5_hash = replay_hash
        self.mods = Mods(score_info["mods"])
        self.timestamp = score_info["timestamp"]
        self.online_id = score_info["online_id"]
        self.pp = None

    def get_pp(self):
        pp_map = self.client.get_local_map(self.map_hash)
        if pp_map:
            self.pp = pp_map.get_pp(self)
        return self.pp

    def __repr__(self):
        return f"{self.mods} score by {self.username}"
