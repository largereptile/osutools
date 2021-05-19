from .utils import *
from .map import LocalMap
from .score import LocalScore


class OsuDB:
    def __init__(self, client, path):
        self.client = client
        with open(path, "rb") as db:
            self.version = read_int(db)
            self.folder_count = read_int(db)
            self.account_unlocked = read_bool(db)
            self.date_unlocked = read_long(db)
            self.player_name = read_string(db)
            self.number_of_beatmaps = read_int(db)
            self.maps = {}
            self.maps_by_hash = {}
            for _ in range(self.number_of_beatmaps):
                map_info = {}
                if self.version < 20191106:
                    map_info["file_size"] = read_int(db)
                else:
                    map_info["file_size"] = -1
                map_info["osu_version"] = self.version
                map_info["artist"] = read_string(db)
                map_info["artist_unicode"] = read_string(db)
                map_info["title"] = read_string(db)
                map_info["title_unicode"] = read_string(db)
                map_info["creator"] = read_string(db)
                map_info["version"] = read_string(db)  # difficulty name
                map_info["audio_filename"] = read_string(db)
                map_info["file_md5"] = read_string(db)
                map_info["filename"] = read_string(db)
                ranked_status = read_byte(db)  # why is this different to the online api
                map_info["approved"] = ranked_status - 3 if ranked_status >= 4 else -2
                map_info["count_normal"] = read_short(db)
                map_info["count_slider"] = read_short(db)
                map_info["count_spinner"] = read_short(db)
                map_info["last_mod_time"] = read_long(db)
                if self.version < 20140609:
                    map_info["diff_approach"] = int(read_byte(db))
                    map_info["diff_size"] = int(read_byte(db))
                    map_info["diff_drain"] = int(read_byte(db))
                    map_info["diff_overall"] = int(read_byte(db))
                else:
                    map_info["diff_approach"] = read_single(db)
                    map_info["diff_size"] = read_single(db)
                    map_info["diff_drain"] = read_single(db)
                    map_info["diff_overall"] = read_single(db)
                map_info["slider_velocity"] = read_double(db)
                if self.version >= 20140609:
                    no_pairs = read_int(db)
                    map_info["standard_star_ratings"] = [read_int_double(db) for _ in range(no_pairs)]
                    no_pairs = read_int(db)
                    map_info["taiko_star_ratings"] = [read_int_double(db) for _ in range(no_pairs)]
                    no_pairs = read_int(db)
                    map_info["ctb_star_ratings"] = [read_int_double(db) for _ in range(no_pairs)]
                    no_pairs = read_int(db)
                    map_info["mania_star_ratings"] = [read_int_double(db) for _ in range(no_pairs)]
                map_info["drain_time"] = read_int(db)
                map_info["total_length"] = read_int(db)
                map_info["preview_start_time"] = read_int(db)
                no_timing = read_int(db)
                map_info["timing_points"] = [read_timing(db) for _ in range(no_timing)]
                map_info["beatmap_id"] = read_int(db)
                map_info["beatmapset_id"] = read_int(db)
                map_info["thread_id"] = read_int(db)
                map_info["best_grade_standard"] = read_byte(db)
                map_info["best_grade_taiko"] = read_byte(db)
                map_info["best_grade_ctb"] = read_byte(db)
                map_info["best_grade_mania"] = read_byte(db)
                map_info["local_offset"] = read_short(db)
                map_info["stack_leniency"] = read_single(db)
                map_info["mode"] = read_byte(db)
                map_info["source"] = read_string(db)
                map_info["tags"] = read_string(db)
                map_info["online_offset"] = read_short(db)
                map_info["title_font"] = read_string(db)
                map_info["unplayed"] = read_bool(db)
                map_info["last_played"] = read_long(db)
                map_info["is_osz2"] = read_bool(db)
                map_info["folder_name"] = read_string(db)
                map_info["last_updated"] = read_long(db)
                map_info["ignore_sound"] = read_bool(db)
                map_info["ignore_skin"] = read_bool(db)
                map_info["disable_storyboard"] = read_bool(db)
                map_info["disable_video"] = read_bool(db)
                map_info["visual_override"] = read_bool(db)
                if self.version < 20140609:
                    read_short(db)  # wiki says this just isn't actually a used value
                map_info["last_mod_time_2"] = read_int(db)
                map_info["scroll_speed"] = read_byte(db)
                mp = LocalMap(map_info, client)
                self.maps[mp.beatmap_id] = mp
                self.maps_by_hash[mp.md5_hash] = mp

    def search_maps(self, name: str):
        results = []
        name = name.lower()
        for local_map in self.maps.values():
            if name in local_map.song_title.lower():
                results.append(local_map)
        return results

    def get_map_from_hash(self, md5_hash: str):
        for local_map in self.maps.values():
            if local_map.md5_hash == md5_hash:
                return local_map
        return None


class Collections:
    def __init__(self, path, client):
        self.client = client
        with open(path, "rb") as db:
            self.version = read_int(db)
            self.collections = {}
            no_collections = read_int(db)
            for _ in range(no_collections):
                collection = []
                name = read_string(db)
                no_maps = read_int(db)
                for _ in range(no_maps):
                    collection.append(read_string(db))
                self.collections[name] = collection


class ScoresDB:
    def __init__(self, path, client):
        self.client = client
        with open(path, "rb") as db:
            self.version = read_int(db)
            no_maps = read_int(db)
            self.maps = {}
            for _ in range(no_maps):
                md5 = read_string(db)
                scores = []
                no_scores = read_int(db)
                for _ in range(no_scores):
                    score_info = {"mode": read_byte(db), "version": read_int(db)}
                    map_md5 = read_string(db)
                    score_info["username"] = read_string(db)
                    score_info["replay_hash"] = read_string(db)
                    score_info["count300"] = read_short(db)
                    score_info["count100"] = read_short(db)
                    score_info["count50"] = read_short(db)
                    score_info["countgeki"] = read_short(db)
                    score_info["countkatu"] = read_short(db)
                    score_info["countmiss"] = read_short(db)
                    score_info["score"] = read_int(db)
                    score_info["maxcombo"] = read_short(db)
                    score_info["perfect"] = read_bool(db)
                    score_info["mods"] = read_int(db)
                    read_string(db)
                    score_info["timestamp"] = read_long(db)
                    read_int(db)
                    score_info["online_id"] = read_long(db)
                    if Mods.Target & Mods(score_info["mods"]):
                        score_info["target_practice_acc"] = read_double(db)

                    scores.append(LocalScore(score_info, client, score_info["replay_hash"]))

                self.maps[md5] = scores

