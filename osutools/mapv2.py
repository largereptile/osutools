import tempfile
import urllib.request
import os
from .utils import *
from .oppai import Oppai

# TODO: make timestamps actual timestamps


class MapCompactV2:
    def __init__(self, client, params) -> None:
        self.client = client
        self.star_rating = float(params["difficulty_rating"])
        self.id = int(params["id"])
        self.mode_text = params["mode"]
        self.length = int(params["total_length"])
        self.difficulty_name = params["version"]
        self.approval_text = params["status"]
        self.md5_hash = params["checksum"] if "checksum" in params.keys() else None
        self.failtimes = params["failtimes"] if "failtimes" in params.keys() else None
        self.max_combo = params["max_combo"] if "max_combo" in params.keys() else 0
        if "beatmapset" in params.keys():
            mapset = params["beatmapset"]
            if "availability" in mapset.keys():
                self.beatmapset = BeatmapsetV2(client, mapset)
            else:
                self.beatmapset = BeatmapsetCompactV2(client, mapset)
            self.repr_string = f"{self.beatmapset.song_title} [{self.difficulty_name}] mapped by {self.beatmapset.creator_name}"
        else:
            self.beatmapset = None
            self.repr_string = f"Map Id: {self.id}"

    def __repr__(self):
        return self.repr_string


class MapV2(MapCompactV2):
    def __init__(self, client, params) -> None:
        self.overall_difficulty = float(params["accuracy"])
        self.approach_rate = float(params["ar"])
        self.mapset_id = int(params["beatmapset_id"])
        self.bpm = float(params["bpm"])
        self.convert = bool(params["convert"])
        self.circle_count = int(params["count_circles"])
        self.slider_count = int(params["count_sliders"])
        self.spinner_count = int(params["count_spinners"])
        self.total_objects = self.circle_count + self.slider_count + self.spinner_count
        self.circle_size = float(params["cs"])
        self.deleted_at = (
            None if params["deleted_at"] == "null" else params["deleted_at"]
        )
        self.hp_drain = float(params["drain"])
        self.no_break_length = int(params["hit_length"])
        self.is_scoreable = bool(params["is_scoreable"])
        self.last_updated = params["last_updated"]
        self.mode = Mode(int(params["mode_int"]))
        self.passcount = int(params["passcount"])
        self.playcount = int(params["playcount"])
        self.approval = Approval(int(params["ranked"]))
        self.url = params["url"]
        super().__init__(client, params)


class BeatmapPlaycount:
    def __init__(self) -> None:
        pass


class BeatmapScores:
    def __init__(self) -> None:
        pass


class BeatmapUserScore:
    def __init__(self) -> None:
        pass


class BeatmapsetCompactV2:
    def __init__(self, client, params) -> None:
        self.client = client
        self.artist = params["artist"]
        self.artist_unicode = params["artist_unicode"]
        self.covers = params["covers"]
        self.creator_name = params["creator"]
        self.favourites = int(params["favourite_count"])
        self.id = int(params["id"])
        self.nsfw = bool(params["nsfw"])
        self.playcount = int(params["play_count"])
        self.preview_url = params["preview_url"]
        self.source = params["source"]
        self.approval_string = params["status"]
        self.song_title = params["title"]
        self.song_title_unicode = params["title_unicode"]
        self.creator_id = int(params["user_id"])
        self.video = bool(params["video"])
        self.beatmaps = (
            [MapV2(client, m) for m in params["beatmaps"]]
            if "beatmaps" in params.keys()
            else None
        )
        self.converts = params["converts"] if "converts" in params.keys() else None
        self.current_user_attributes = (
            params["current_user_attributes"]
            if "current_user_attributes" in params.keys()
            else None
        )
        self.description = (
            params["description"] if "description" in params.keys() else None
        )
        self.discussions = (
            params["discussions"] if "discussions" in params.keys() else None
        )
        self.events = params["events"] if "events" in params.keys() else None
        self.genre = params["genre"] if "genre" in params.keys() else None
        self.has_favourited = (
            bool(params["has_favourited"])
            if "has_favourited" in params.keys()
            else None
        )
        self.language = params["language"] if "language" in params.keys() else None
        self.nominations = (
            params["nominations"] if "nominations" in params.keys() else None
        )
        self.ratings = params["ratings"] if "ratings" in params.keys() else None
        self.recent_favourites = (
            params["recent_favourites"]
            if "recent_favourites" in params.keys()
            else None
        )
        self.related_users = (
            params["related_users"] if "related_users" in params.keys() else None
        )
        self.user = params["user"] if "user" in params.keys() else None


class BeatmapsetV2(BeatmapsetCompactV2):
    def __init__(self, client, params) -> None:
        self.availability = Availability(params["availability"])
        self.bpm = float(params["bpm"])
        self.can_be_hyped = bool(params["can_be_hyped"])
        self.creator_name = params["creator"]
        self.discussion_enabled = bool(params["discussion_enabled"])
        self.discussion_locked = bool(params["discussion_locked"])
        self.hype = Hype(params["hype"]) if params["hype"] else None
        self.is_scoreable = bool(params["is_scoreable"])
        self.last_updated = params["last_updated"]
        self.legacy_thread_url = (
            None
            if params["legacy_thread_url"] == "null"
            else params["legacy_thread_url"]
        )
        self.nominations = Nominations(params["nominations_summary"])
        self.approval = Approval(int(params["ranked"]))
        self.ranked_date = params["ranked_date"]
        self.source = params["source"]
        self.storyboard = bool(params["storyboard"])
        self.date_submitted = params["submitted_date"]
        self.tags = params["tags"].split(" ")
        self.has_favourited = (
            params["has_favourited"] if "has_favourited" in params.keys() else None
        )
        super().__init__(client, params)


class Availability:
    def __init__(self, params):
        self.download_disabled = bool(params["download_disabled"])
        self.more_information = (
            None if params["more_information"] == "null" else params["more_information"]
        )


class Hype:
    def __init__(self, params):
        self.current = int(params["current"])
        self.required = int(params["required"])


class Nominations:
    def __init__(self, params) -> None:
        self.current = int(params["current"])
        self.required = int(params["required"])


class BeatmapsetDiscussion:
    def __init__(self) -> None:
        pass


class BeatmapsetDiscussionPost:
    def __init__(self) -> None:
        pass


class BeatmapsetDiscussionVote:
    def __init__(self) -> None:
        pass
