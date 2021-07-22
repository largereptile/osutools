from datetime import datetime, timedelta
from .utils import Mode, Playtime


class User:
    """Object representing JSON response from the osu! api plus some helper methods.

    Attributes:
        client: OsuClient that created the instance
        mode: enum representing the osu! gamemode this information is for
        id: id of the player
        username: player's username
        join_date: timestamp of when the player created their account
        num_300: number of 300s player has achieved
        num_100: number of 100s player has achieved
        num_50: number of 50s player has achieved
        play_count: the number of "plays" according to however osu! calculates it
        ranked_score: combination of highest submitted scores on ranked maps
        total_score: combination of highest submitted scores across all online maps
        rank: the position of the player on the global leaderboard based on their pp
        level: the player's level
        pp: the player's pp total (points received from ranked maps)
        accuracy: the player's average accuracy on a map as a percentage
        ss_count: number of SS's
        ssh_count: number of SS's with hidden
        s_count: number of S ranks
        sh_count: number of S ranks with hidden
        a_count: number of A ranks
        country: the country the player is from
        playtime: Playtime object representing how long they have played the game
        recents: dict containing a list of cached recent scores for each mode
        avatar_url: the url for their profile picture

    """

    def __init__(self, user_info, osu_client, mode: Mode = Mode.STANDARD):
        self.client = osu_client
        self.mode = mode
        self.id = int(user_info["user_id"])
        self.username = user_info["username"]
        self.join_date = datetime.strptime(user_info["join_date"], "%Y-%m-%d %H:%M:%S")
        self.num_300 = int(user_info["count300"])
        self.num_100 = int(user_info["count100"])
        self.num_50 = int(user_info["count50"])
        self.play_count = int(user_info["playcount"])
        self.ranked_score = int(user_info["ranked_score"])
        self.total_score = int(user_info["total_score"])
        self.rank = int(user_info["pp_rank"])
        self.level = float(user_info["level"])
        self.pp = float(user_info["pp_raw"])
        self.accuracy = float(user_info["accuracy"])
        self.ss_count = int(user_info["count_rank_ss"])
        self.ssh_count = int(user_info["count_rank_ssh"])
        self.s_count = int(user_info["count_rank_s"])
        self.sh_count = int(user_info["count_rank_sh"])
        self.a_count = int(user_info["count_rank_a"])
        self.country_code = user_info["country"]
        self.country_rank = int(user_info["pp_country_rank"])
        seconds = int(user_info["total_seconds_played"])
        self.playtime = Playtime(seconds)
        self.recents = {Mode.STANDARD: [], Mode.TAIKO: [], Mode.CTB: [], Mode.MANIA: []}
        self.avatar_url = f"http://s.ppy.sh/a/{self.id}"

    def fetch_best(self, mode: Mode = Mode.STANDARD, limit: int = 10):
        """Helper for collecting a user's best scores.

        Args:
            mode: enum representing osu! gamemode to request scores for
            limit: number of scores to retrieve (max 100)

        Returns:
            [Score]: List of the player's best scores
        """
        return self.client.fetch_user_best(user_id=self.id, mode=mode, limit=limit)

    def fetch_recent(self, mode: Mode = Mode.STANDARD, limit: int = 10):
        """Helper for collecting a user's recent scores.

        Args:
            mode: enum representing osu! gamemode to request scores for
            limit: number of scores to retrieve (max 100)

        Returns:
            [RecentScore]: List of the player's recent scores
        """
        self.recents[mode] = self.client.fetch_user_recent(
            user_id=self.id, mode=mode, limit=limit
        )
        return self.recents[mode]

    def fetch_new_recent(self, mode: Mode = Mode.STANDARD):
        """Retrieve any scores made since the last time this function was called.

        Args:
            mode: enum representing osu! gamemode to request scores for

        Returns:
            [RecentScore]: List of the player's scores since the most recent
        """
        now = datetime.now()
        self.recents[mode] = [
            score
            for score in self.recents[mode]
            if (now - timedelta(hours=24)) <= score.timestamp <= now
        ]
        new_scores = self.client.fetch_user_recent(
            user_id=self.id, mode=mode, limit=100
        )
        if new_scores:
            dates = [score.timestamp for score in self.recents[mode]]
            new = [score for score in new_scores if score.timestamp not in dates]
            self.recents[mode] += new
            return new

    def __repr__(self):
        return self.username
