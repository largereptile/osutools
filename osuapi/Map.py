from datetime import datetime
from .Utils import *


class Map:
    def __init__(self, map_info, client):
        self.client = client

        self.song_title = map_info['title']
        self.artist = map_info['artist']
        self.bpm = int(map_info['bpm'])
        self.genre = Genre(int(map_info['genre_id']))
        self.length = float(map_info['total_length'])
        self.language = Language(int(map_info['language_id']))

        self.difficulty_name = map_info['version']
        self.mode = Mode(int(map_info['mode']))
        self.beatmap_id = int(map_info['beatmap_id'])
        self.mapset_id = int(map_info['beatmapset_id'])
        self.creator_name = map_info['creator']
        self.creator_id = int(map_info['creator_id'])
        self.tags = map_info['tags'].split(" ")
        self.cover_image_url = f"https://assets.ppy.sh/beatmaps/{self.mapset_id}/covers/cover.jpg"
        self.thumbnail = f"https://b.ppy.sh/thumb/{self.mapset_id}l.jpg"

        self.favourites = int(map_info['favourite_count'])
        self.rating = float(map_info['rating'])
        self.playcount = int(map_info['playcount'])
        self.passcount = int(map_info['passcount'])

        self.approval = Approval(int(map_info['approved']))
        self.date_submitted = datetime.strptime(map_info['submit_date'], "%Y-%m-%d %H:%M:%S")
        self.date_approved = datetime.strptime(map_info['approved_date'], "%Y-%m-%d %H:%M:%S")
        self.last_update = datetime.strptime(map_info['last_update'], "%Y-%m-%d %H:%M:%S")

        self.star_rating = float(map_info['difficultyrating'])
        self.aim_difficulty = float(map_info['diff_aim'])
        self.speed_difficulty = float(map_info['diff_speed'])
        self.circle_size = float(map_info['diff_size'])
        self.overall_difficulty = float(map_info['diff_overall'])
        self.approach_rate = float(map_info['diff_approach'])
        self.hp_drain = float(map_info['diff_drain'])
        self.no_break_length = float(map_info['hit_length'])
        self.source = map_info['source']
        self.circle_count = int(map_info['count_normal'])
        self.slider_count = int(map_info['count_slider'])
        self.spinner_count = int(map_info['count_spinner'])
        self.total_objects = self.circle_count + self.slider_count + self.spinner_count
        self.max_combo = int(map_info['max_combo'])

        self.storyboard = map_info['storyboard'] == "1"
        self.video = map_info['video'] == "1"
        self.download_unavailable = map_info['download_unavailable'] == "1"
        self.audio_unavailable = map_info['audio_unavailable'] == "1"
        self.md5_hash = map_info['file_md5']

    def __repr__(self):
        return f"{self.song_title} mapped by {self.creator_name}"

    def fetch_creator(self):
        return self.client.get_user(self.creator_id)

    def fetch_mapset(self):
        pass