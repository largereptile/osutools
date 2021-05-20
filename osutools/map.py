import tempfile
import urllib.request
import pyttanko
from .utils import *
from .oppai import Oppai


class BaseMap:
    def __init__(self, map_info, client):
        self.client = client
        self.song_title = map_info['title']
        self.artist = map_info['artist']
        self.length = float(map_info['total_length']) if float(map_info['total_length']) != 4294967295 else 0
        self.difficulty_name = map_info['version']
        self.mode = Mode(int(map_info['mode']))
        self.beatmap_id = int(map_info['beatmap_id'])
        self.mapset_id = int(map_info['beatmapset_id'])
        self.creator_name = map_info['creator']
        self.tags = map_info['tags'].split(" ")
        self.approval = Approval(int(map_info['approved']))
        self.circle_size = float(map_info['diff_size'])
        self.overall_difficulty = float(map_info['diff_overall'])
        self.approach_rate = float(map_info['diff_approach'])
        self.hp_drain = float(map_info['diff_drain'])
        self.source = map_info['source']
        self.circle_count = int(map_info['count_normal'])
        self.slider_count = int(map_info['count_slider'])
        self.spinner_count = int(map_info['count_spinner'])
        self.total_objects = self.circle_count + self.slider_count + self.spinner_count
        self.md5_hash = map_info['file_md5']

    def __repr__(self):
        return f"{self.song_title} [{self.difficulty_name}] mapped by {self.creator_name}"


class LocalMap(BaseMap):
    def __init__(self, map_info, client):
        self.filesize = map_info["file_size"]
        self.artist_unicode = map_info["artist_unicode"]
        self.title_unicode = map_info["title_unicode"]
        self.osu_version = map_info["osu_version"]
        self.audio_filename = map_info["audio_filename"]
        self.filename = map_info["filename"]
        self.last_mod_time = map_info["last_mod_time"]
        # self.last_mod_time_2 = map_info["last_mod_time_2"]
        self.slider_velocity = map_info["slider_velocity"]
        if int(self.osu_version) >= 20140609:
            self.standard_sr_ratings = map_info["standard_star_ratings"]
            self.taiko_sr_ratings = map_info["taiko_star_ratings"]
            self.ctb_sr_ratings = map_info["ctb_star_ratings"]
            self.mania_sr_ratings = map_info["mania_star_ratings"]
        self.drain_time = map_info["drain_time"]
        self.preview_start = map_info["preview_start_time"]
        self.timing_points = map_info["timing_points"]
        self.thread_id = map_info["thread_id"]
        self.best_grade_standard = map_info["best_grade_standard"]
        self.best_grade_taiko = map_info["best_grade_taiko"]
        self.best_grade_ctb = map_info["best_grade_ctb"]
        self.best_grade_mania = map_info["best_grade_mania"]
        self.local_offset = map_info["local_offset"]
        self.stack_leniency = map_info["stack_leniency"]
        self.online_offset = map_info["online_offset"]
        self.title_font = map_info["title_font"]
        self.unplayed = map_info["unplayed"]
        self.last_played = map_info["last_played"]
        self.is_osz2 = map_info["is_osz2"]
        self.folder_name = map_info["folder_name"]
        self.last_updated = map_info["last_updated"]
        self.ignore_sound = map_info["ignore_sound"]
        self.ignore_skin = map_info["ignore_skin"]
        self.disable_storyboard = map_info["disable_storyboard"]
        self.disable_video = map_info["disable_video"]
        self.visual_override = map_info["visual_override"]
        if map_info["mode"] == 3:
            self.scroll_speed = map_info["scroll_speed"]

        super().__init__(map_info, client)

    def get_pp(self, score):
        """
        Return the maximum PP value for the map with the supplied mods, or the PP for a given score on the map
        Args:
            score: Score to calculate PP for
            mods: enum representing mods to filter by

        Returns:
            float: Maximum PP for the map.
        """
        filename = f"{self.client.osu_folder}\\Songs\\{self.folder_name.strip()}\\{self.filename}"

        return Oppai.calculate_pp(filename, mods=score.mods.value, max_combo=score.max_combo, misses=score.misses,
                                  num_100=score.num_100, num_50=score.num_50)

    def get_local_scores(self):
        if self.md5_hash in self.client.scores_db.maps.keys():
            return self.client.scores_db.maps[self.md5_hash]
        return []

    def get_online_map(self):
        return self.client.fetch_map(self.beatmap_id)


class Map(BaseMap):
    def __init__(self, map_info, client):
        super().__init__(map_info, client)
        self.bpm = float(map_info['bpm'])
        self.genre = Genre(int(map_info['genre_id']))
        self.language = Language(int(map_info['language_id']))
        self.creator_id = int(map_info['creator_id'])
        self.favourites = int(map_info['favourite_count'])
        self.rating = float(map_info['rating'])
        self.playcount = int(map_info['playcount'])
        self.passcount = int(map_info['passcount'])
        self.date_submitted = datetime.strptime(map_info['submit_date'], "%Y-%m-%d %H:%M:%S")
        self.date_approved = datetime.strptime(map_info['approved_date'], "%Y-%m-%d %H:%M:%S") if map_info[
            'approved_date'] else None
        self.last_update = datetime.strptime(map_info['last_update'], "%Y-%m-%d %H:%M:%S")
        self.star_rating = float(map_info['difficultyrating'])
        self.aim_difficulty = float(map_info['diff_aim'])
        self.speed_difficulty = float(map_info['diff_speed'])
        self.no_break_length = float(map_info['hit_length'])
        self.max_combo = int(map_info['max_combo'])
        self.storyboard = map_info['storyboard'] == "1"
        self.video = map_info['video'] == "1"
        self.download_unavailable = map_info['download_unavailable'] == "1"
        self.audio_unavailable = map_info['audio_unavailable'] == "1"
        self.download_url = f"https://osu.ppy.sh/osu/{self.beatmap_id}"
        self.cover_image_url = f"https://assets.ppy.sh/beatmaps/{self.mapset_id}/covers/cover.jpg"
        self.thumbnail = f"https://b.ppy.sh/thumb/{self.mapset_id}l.jpg"

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
        return self.client.fetch_scores(self.beatmap_id, username=username, user_id=user_id,
                                        mode=mode, mods=mods, limit=limit)

    def get_pp(self, score=None, mods=Mods.NM):
        """
        Return the maximum PP value for the map with the supplied mods, or the PP for a given score on the map
        Args:
            score: Score to calculate PP for
            mods: enum representing mods to filter by

        Returns:
            float: Maximum PP for the map.
        """
        temp_map = tempfile.NamedTemporaryFile(delete=False)
        temp_map.write(urllib.request.urlopen(self.download_url).read())
        temp_map.close()
        try:
            if score:
                pp_out = Oppai.calculate_pp(temp_map.name, mods=score.mods.value, max_combo=score.max_combo,
                                            misses=score.misses, num_100=score.num_100, num_50=score.num_50)
            else:
                pp_out = Oppai.calculate_pp(temp_map.name, mods=mods.value)
        finally:
            os.remove(temp_map.name)
        return pp_out
