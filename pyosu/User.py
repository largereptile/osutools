from datetime import datetime, timedelta
from .Utils import Mode, Playtime


class User:
    def __init__(self, user_info, osu_client, mode: Mode = Mode.STANDARD):
        self.client = osu_client
        self.mode = mode
        self.id = int(user_info['user_id'])
        self.username = user_info['username']
        self.join_date = datetime.strptime(user_info['join_date'], "%Y-%m-%d %H:%M:%S")
        self.num_300 = int(user_info['count300'])
        self.num_100 = int(user_info['count100'])
        self.num_50 = int(user_info['count50'])
        self.play_count = int(user_info['playcount'])
        self.ranked_score = int(user_info['ranked_score'])
        self.total_score = int(user_info['total_score'])
        self.rank = int(user_info['pp_rank'])
        self.level = float(user_info['level'])
        self.pp = float(user_info['pp_raw'])
        self.accuracy = float(user_info['accuracy'])
        self.ss_count = int(user_info['count_rank_ss'])
        self.ssh_count = int(user_info['count_rank_ssh'])
        self.s_count = int(user_info['count_rank_s'])
        self.sh_count = int(user_info['count_rank_sh'])
        self.a_count = int(user_info['count_rank_a'])
        self.country = user_info['country']
        self.country_rank = int(user_info['pp_country_rank'])
        seconds = int(user_info['total_seconds_played'])
        self.playtime = Playtime(seconds)
        self.recents = {
            Mode.STANDARD: [],
            Mode.TAIKO: [],
            Mode.CTB: [],
            Mode.MANIA: []
        }
        self.avatar_url = f"http://s.ppy.sh/a/{self.id}"

    def fetch_best(self, mode: Mode = Mode.STANDARD, limit: int = 10):
        return self.client.fetch_user_best(user_id=self.id, mode=mode, limit=limit)

    def fetch_recent(self, mode: Mode = Mode.STANDARD, limit: int = 10):
        self.recents[mode] = self.client.fetch_user_recent(user_id=self.id, mode=mode, limit=limit)
        return self.recents[mode]

    def fetch_new_recent(self, mode: Mode = Mode.STANDARD):
        now = datetime.now()
        self.recents[mode] = [score for score in self.recents[mode] if (now - timedelta(hours=24)) <= score.timestamp <= now]
        new_scores = self.client.fetch_user_recent(user_id=self.id, mode=mode, limit=100)
        if new_scores:
            dates = [score.timestamp for score in self.recents[mode]]
            new = [score for score in new_scores if score.timestamp not in dates]
            self.recents[mode] += new
            return new

    def __repr__(self):
        return self.username

