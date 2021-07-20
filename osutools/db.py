import json

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
            self.date_unlocked = read_datetime(db)
            self.player_name = read_string(db)
            self.number_of_beatmaps = read_int(db)
            self.maps = {}
            self.map_dicts = {}
            self.id_to_hash = {}
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
                map_info["last_mod_time"] = read_datetime(db)
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
                self.map_dicts[mp.beatmap_id] = map_info
                self.maps[mp.md5_hash] = mp
                self.id_to_hash[mp.beatmap_id] = mp.md5_hash

    def map_list(self):
        return list(self.maps.values())

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

    def export(self, path=None):
        if not path:
            path = "osu_db.json"
        db_dict = self.__dict__.copy()
        db_dict.pop("client")
        db_dict.pop("maps")
        db_dict.pop("id_to_hash")
        json_str = json.dumps(db_dict, sort_keys=True, indent=4, default=str)
        with open(path, "w") as f:
            f.write(json_str)


class Collections:
    def __init__(self, client, path):
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

    def export(self, path=None):
        if not path:
            path = "collection.json"
        db_dict = self.__dict__.copy()
        db_dict.pop("client")
        json_str = json.dumps(db_dict, sort_keys=True, indent=4, default=str)
        with open(path, "w") as f:
            f.write(json_str)


class ScoresDB:
    def __init__(self, client, path):
        self.client = client
        with open(path, "rb") as db:
            self.version = read_int(db)
            no_maps = read_int(db)
            self.maps = {}
            self.score_by_map = {}
            for _ in range(no_maps):
                md5 = read_string(db)
                scores = []
                score_dict = []
                no_scores = read_int(db)
                for _ in range(no_scores):

                    score_info = {"mode": read_byte(db), "version": read_int(db), "map_hash": read_string(db),
                                  "username": read_string(db), "replay_hash": read_string(db),
                                  "count300": read_short(db), "count100": read_short(db), "count50": read_short(db),
                                  "countgeki": read_short(db), "countkatu": read_short(db), "countmiss": read_short(db),
                                  "score": read_int(db), "maxcombo": read_short(db), "perfect": read_bool(db),
                                  "mods": read_int(db)}
                    read_string(db)
                    score_info["timestamp"] = read_datetime(db)
                    read_int(db)
                    score_info["online_id"] = read_long(db)
                    if Mods.Target & Mods(score_info["mods"]):
                        score_info["target_practice_acc"] = read_double(db)

                    scores.append(LocalScore(score_info, client, score_info["replay_hash"]))
                    score_dict.append(score_info)
                if score_dict and scores[0].map:
                    map_id = scores[0].map.beatmap_id
                    self.score_by_map[map_id] = score_dict
                self.maps[md5] = scores

    def load_pp(self):
        for md5, scores in self.maps.items():
            for score in scores:
                score.get_pp()

    def get_scores_before(self, timestamp, names=None, ranked_only=False):
        before_timestamp = {}
        for md5, scores in self.maps.items():
            if ranked_only:
                if ranked_only:
                    beatmap = self.client.get_local_map(md5)
                    if beatmap.approval != Approval.RANKED:
                        continue
            scores_before = list(filter(lambda x: x.timestamp < timestamp, scores))
            if names:
                scores_before = list(filter(lambda x: x.username in names, scores_before))
            if scores_before:
                before_timestamp[md5] = scores_before
        return before_timestamp

    def get_best_scores_before(self, timestamp, names=None, ranked_only=False):
        if not names:
            names = [self.client.osu_db.player_name]
        all_scores = self.get_scores_before(timestamp, names=names, ranked_only=ranked_only)
        best_scores = []
        for md5, scores in all_scores.items():
            try:
                scores.sort(key=lambda x: x.score, reverse=True)
                if not scores:
                    continue
                best = scores[0]
                if not best.pp:
                    best.get_pp()
                if best.pp:
                    best_scores.append(best)
            except NotImplementedError:
                pass
            except ValueError:
                pass
        best_scores.sort(key=lambda x: x.pp, reverse=True)
        return best_scores[:100]

    def export(self, path=None):
        if not path:
            path = "scores.json"
        db_dict = self.__dict__.copy()
        db_dict.pop("client")
        db_dict.pop("maps")
        json_str = json.dumps(db_dict, sort_keys=True, indent=4, default=str)
        with open(path, "w") as f:
            f.write(json_str)
