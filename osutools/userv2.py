from .utils import Mode

# TODO: make times actual timestamps

class UserCompactV2:
    def __init__(self, client, params) -> None:
        self.client = client
        self.avatar_url = params.get("avatar_url")
        self.country_code = params["country_code"]
        self.default_group = params.get("default_group")  # UserGroup(params["default_group"])
        self.id = int(params["id"])
        self.is_active = params["is_active"]
        self.is_bot = params["is_bot"]
        self.is_deleted = params["is_deleted"]
        self.is_online = params["is_online"]
        self.is_supporter = params["is_supporter"]
        self.last_visit = params["last_visit"]
        self.pm_friends_only = params["pm_friends_only"]
        self.profile_colour = params["profile_colour"]
        self.username = params["username"]
        self.account_history = params.get("account_history", [])
        self.active_tournament_banner = params.get("active_tournament_banner", None)
        self.badges = params.get("badges", [])
        self.beatmap_playcounts_count = params.get("beatmap_playcounts_count", 0)
        self.blocks = params.get("blocks", None)
        self.country = params.get("country", None)
        self.cover = params.get("cover", None)
        self.favourite_beatmapset_count = params.get("favourite_beatmapset_count", 0)
        self.follower_count = params.get("follower_count", 0)
        self.friends = params.get("friends", 0)
        self.graveyard_beatmapset_count = params.get("graveyard_beatmapset_count", 0)
        self.groups = map(lambda x: UserGroup(x), params.get("groups", []))
        self.is_restricted = params.get("is_restricted", False)
        self.loved_beatmapset_count = params.get("loved_beatmapset_count", 0)
        self.monthly_playcounts = params.get("monthly_playcounts", [])
        self.page = params.get("page", None)
        self.pending_beatmapset_count = params.get("pending_beatmapset_count", 0)
        self.previous_usernames = params.get("previous_usernames", [])
        self.rank_history = params.get("rank_history", None)
        self.ranked_beatmapset_count = params.get("ranked_beatmapset_count", 0)
        self.replays_watched_counts = params.get("replays_watched_counts", 0)
        self.scores_best_count = params.get("scores_best_count", 0)
        self.scores_first_count = params.get("scores_first_count", 0)
        self.scores_recent_count = params.get("scores_recent_count", 0)
        self.statistics = UserStatistics(params.get("statistics", {}))
        self.statistics_rulesets = params.get("statistics_rulesets", None)
        self.support_level = params.get("support_level", 0)
        self.unread_pm_count = params.get("unread_pm_count", 0)
        self.user_achievements = params.get("user_achievements", None)
        self.user_preferences = params.get("user_preferences", None)


class UserV2(UserCompactV2):
    def __init__(self, client, params) -> None:
        self.cover_url = params.get("cover", {}).get("url", None)
        self.discord = params.get("discord", None)
        self.has_supported = params.get("has_supported", False)
        self.interests = params.get("interests", None)
        self.join_date = params.get("join_date", None)
        self.kudosu_available = params.get("kudosu", {}).get("available", 0)
        self.kudosu_total = params.get("kudosu", {}).get("total", 0)
        self.location = params.get("location", None)
        self.max_blocks = params.get("max_blocks", 0)
        self.max_friends = params.get("max_friends", 0)
        self.occupation = params.get("occupation", None)
        playmode = params.get("playmode", "osu")
        if playmode == "mania":
            self.playmode = Mode.MANIA
        elif playmode == "taiko":
            self.playmode = Mode.TAIKO
        elif playmode == "ctb":
            self.playmode = Mode.CTB
        else:
            self.playmode = Mode.STANDARD
        self.playstyle = params.get("playstyle", [])
        self.post_count = params.get("post_count", 0)
        self.title = params.get("title", None)
        self.title_url = params.get("title_url", None)
        self.twitter = params.get("twitter", None)
        self.website = params.get("website", None)
        super().__init__(client, params)


class UserGroup:
    def __init__(self, params) -> None:
        self.colour = params["colour"]
        self.has_listing = params["has_listing"]
        self.has_playmodes = params["has_playmodes"]
        self.id = params["id"]
        self.identifier = params["identifier"]
        self.is_probationary = params["is_probationary"]
        self.name = params["name"]
        self.short_name = params["short_name"]
        self.description = params.get("description", "")


class UserStatistics:
    def __init__(self, params) -> None:
        self.grade_counts = {
            "a": params.get("grade_counts", {}).get("a", 0),
            "s": params.get("grade_counts", {}).get("s", 0),
            "sh": params.get("grade_counts", {}).get("sh", 0),
            "ss": params.get("grade_counts", {}).get("ss", 0),
            "ssh": params.get("grade_counts", {}).get("ssh", 0)
        }
        self.hit_accuracy = params.get("hit_accuracy", 0)
        self.is_ranked = params.get("is_ranked", False)
        self.level_current = params.get("level", {}).get("current", 0)
        self.level_progress = params.get("level", {}).get("progress", 0)
        self.maximum_combo = params.get("maximum_combo", 0)
        self.play_count = params.get("play_count", 0)
        self.play_time = params.get("play_time", 0)
        self.pp = params.get("pp", 0)
        self.global_rank = params.get("global_rank", 0)
        self.ranked_score = params.get("ranked_score", 0)
        self.replays_watched_by_others = params.get("replays_watched_by_others", 0)
        self.total_hits = params.get("total_hits", 0)
        self.total_score = params.get("total_score", 0)
