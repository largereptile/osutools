from datetime import datetime
import copy
import math
from .utils import *



class Map:
    """An object holding all the information about a specific beatmap.

    Attributes:
        client: OsuClient that created the instance
        song_title: title of the song
        artist: artist who wrote the song
        bpm: speed of the song
        genre: enum representing the genre the map was tagged with
        length: length of the map in seconds
        language: enum representing the language the map was tagged with
        difficulty_name: the name of this map, not the mapset
        mode: enum representing the osu! gamemode the map is for
        beatmap_id: the id of the map
        mapset_id: the id of the beatmap set
        creator_name: the player who mapped it
        creator_id: the id of the player who mapped it
        tags: list of the tags given to the map
        cover_image_url: the url of the image for the map on the website
        thumbnail: the thumbnail of the map
        favourites: the number of times the map has been favourite-ed
        rating: the average rating of the map
        playcount: number of times the map has been played
        passcount: number of times the map has been passed
        approval: enum representing the stage in the ranking process the map is at
        date_submitted: timestamp of map submission
        date_approved: timestamp of ranked/loved/etc. status. None if not yet approved
        last_update: timestamp of when the map was last changed
        star_rating: numerical value representing the difficulty of the map overall
        aim_difficulty: numerical value representing the "aim" difficulty of the map
        speed_difficulty: numerical value representing the "speed" difficulty of the map
        circle_size: the size of the circles in the map
        overall_difficulty: the size of the hit windows in which to click each circle
        hp_drain: the speed at which you lose health
        no_break_length: the length of the map you are actually playing
        source: the source of the map (not sure what this means)
        circle_count: number of circles in the map
        slider_count: number of sliders in the map
        spinner_count: number of spinners in the map
        total_objects: the combined number of objects in the map
        max_combo: the maximum combo achievable in the map
        storyboard: boolean representing if the map has a storyboard or not
        video: boolean representing if the map has a video or not
        download_unavailable: boolean representing if the map is now unavailable for download
        audio_unavailable: boolean representing if the map audio is unavailable
        md5_hash: the md5 hash of the map
    """
    def __init__(self, map_info, client):
        self.client = client

        self.song_title = map_info['title']
        self.artist = map_info['artist']
        self.bpm = float(map_info['bpm'])
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
        self.date_approved = datetime.strptime(map_info['approved_date'], "%Y-%m-%d %H:%M:%S") if map_info['approved_date'] else None
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
        return f"{self.song_title} [{self.difficulty_name}] mapped by {self.creator_name}"

    def fetch_creator(self):
        """Makes an api call to get more information about the map creator

        Returns:
            User: user who mapped the map
        """
        return self.client.get_user(self.creator_id)

    def fetch_mapset(self):
        """Makes an api call to get the rest of the maps in the beatmap set

        Returns:
            [Map]: list of maps in the mapset
        """
        return self.client.get_maps(set_id=self.mapset_id)

    def fetch_scores(self, username: str = None, user_id: int = None,
                     mode: Mode = Mode.STANDARD, mods: Mods = None, limit: int = 50):
        """Makes an api call to get scores for the map.

        Args:
            username: username of player to filter by
            user_id: id of player to filter by
            mode: mode to get the scores for
            mods: enum representing the mods to filter by
            limit: number of scores to return (max 100)

        Returns:
            [Score]: scores matching the search requirements on this map
        """
        return self.client.get_scores(self.beatmap_id, username=username, user_id=user_id,
                                      mode=mode, mods=mods, limit=limit)

    def apply_mods(self, mods: Mods):
        od0_ms = 80
        od10_ms = 20
        ar0_ms = 1800
        ar5_ms = 1200
        ar10_ms = 450

        od_ms_step = (od0_ms - od10_ms) / 10
        ar_ms_step1 = (ar0_ms - ar5_ms) / 5
        ar_ms_step2 = (ar5_ms - ar10_ms) / 5

        speed_changing = Mods.DT | Mods.HT | Mods.NC
        map_changing = Mods.HR | Mods.EZ | speed_changing

        if not (mods & map_changing):
            return self

        updated_map = copy.copy(self)

        speed_mul = 1
        if mods & (Mods.DT | Mods.NC):
            speed_mul = 1.5
        if mods & Mods.HT:
            speed_mul *= 0.75

        od_ar_hp_multiplier = 1
        if mods & Mods.HR:
            od_ar_hp_multiplier = 1.4

        if mods & Mods.EZ:
            od_ar_hp_multiplier *= 0.5

        # changing approach rate
        updated_map.approach_rate *= od_ar_hp_multiplier
        if updated_map.approach_rate < 5:
            ar_ms = ar0_ms - ar_ms_step1 * updated_map.approach_rate
        else:
            ar_ms = ar5_ms - ar_ms_step2 * (updated_map.approach_rate - 5)

        ar_ms = min(float(ar0_ms), max(float(ar10_ms), ar_ms))
        ar_ms /= speed_mul

        if ar_ms > ar5_ms:
            updated_map.approach_rate = (ar0_ms - ar_ms) / ar_ms_step1
        else:
            updated_map.approach_rate = 5 + (ar5_ms - ar_ms) / ar_ms_step2

        # changing od
        updated_map.overall_difficulty *= od_ar_hp_multiplier
        od_ms = od0_ms - math.ceil(od_ms_step * updated_map.overall_difficulty)
        od_ms = min(od0_ms, max(od10_ms, od_ms))
        od_ms /= speed_mul
        updated_map.overall_difficulty = (od0_ms - od_ms) / od_ms_step

        # changing cs
        if mods & mods.HR:
            updated_map.circle_size *= 1.3
        elif mods & mods.EZ:
            updated_map.circle_size *= 0.5

        updated_map.circle_size = min(updated_map.circle_size, 10)

        updated_map.hp_drain = min(10.0, updated_map.hp_drain * od_ar_hp_multiplier)

        return updated_map

