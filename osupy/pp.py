import math

from .map import Map
from .utils import Mods
from .score import *


def get_pp(beatmap: Map, score: Score = None, mods: Mods = Mods.NM, combo_reached: int = 0, misses: int = 0,
           num_300s: int = -1, num_100s: int = 0, num_50s: int = 0):
    beatmap = beatmap.apply_mods(mods)
    total_hits = beatmap.total_objects
    if not (num_300s >= 0):
        num_300s = total_hits
    if not combo_reached:
        combo_reached = beatmap.max_combo

    accuracy = (num_50s * 50 + num_100s * 100 + num_300s * 300) / (total_hits * 300) if total_hits != 0 else 0
    accuracy = min(1.0, max(0.0, accuracy))

    if score:
        misses = score.misses
        successful_hits = score.num_50 + score.num_100 + score.num_300
        total_hits = score.misses + successful_hits
        combo_reached = score.max_combo
        accuracy = score.accuracy_dec
        num_50s = score.num_50
        num_100s = score.num_100
        num_300s = score.num_300

    if (mods & Mods.RX) or (mods & Mods.Relax2) or (mods & Mods.Autoplay):
        return 0.0

    multiplier = 1.12

    if mods & Mods.NF:
        multiplier *= max(0.9, 1 - (0.2 * misses))

    if mods & Mods.SO:
        multiplier *= 1 - (beatmap.spinner_count / total_hits) ** 0.85

    aim_value = get_aim_value(beatmap, total_hits, misses, combo_reached, accuracy, mods)
    speed_value = get_speed_value(beatmap, total_hits, misses, combo_reached, accuracy, num_50s, mods)
    acc_value = get_acc_value(beatmap, total_hits, accuracy, num_300s, num_100s, num_50s, mods)

    return (((aim_value ** 1.1) + (speed_value ** 1.1) + (acc_value ** 1.1)) ** (1/1.1)) * multiplier


def get_aim_value(beatmap: Map, total_hits: int, num_misses: int, combo_reached: int, accuracy: float, mods: Mods = Mods.NM):
    raw_aim = beatmap.aim_difficulty
    if mods & Mods.TD:
        raw_aim = raw_aim ** 0.8

    aim_value = ((5 * max(1, raw_aim / 0.0675) - 4) ** 3) / 100000

    length_bonus = 0.95 + 0.4 * min(1.0, total_hits / 2000) + (math.log10(total_hits/2000) * 0.5 if total_hits > 2000 else 0)

    aim_value *= length_bonus

    if num_misses > 0:
        aim_value *= 0.97 * (1 - ((num_misses/total_hits) ** 0.775) ** num_misses)

    if beatmap.max_combo > 0:
        aim_value *= min((combo_reached ** 0.8) / (beatmap.max_combo ** 0.8), 1)

    approach_rate_factor = 0.0
    if beatmap.approach_rate > 10.33:
        approach_rate_factor += 0.4 * (beatmap.approach_rate - 10.33)
    elif beatmap.approach_rate < 8:
        approach_rate_factor += 0.01 * (8 - beatmap.approach_rate)

    aim_value *= 1 + min(approach_rate_factor, approach_rate_factor * (total_hits/1000))

    if mods & Mods.HD:
        aim_value *= 1 + 0.4 * (12 - beatmap.approach_rate)

    if mods & Mods.FL:
        over_500 = (total_hits - 500) / 1200 if total_hits > 500 else 0
        over_200 = 0.3 * min(1.0, (total_hits - 200) / 300) + over_500 if total_hits > 200 else 0
        aim_value *= 1 + 0.35 * min(1.0, total_hits/200) + over_200

    aim_value *= 0.5 + accuracy / 2
    aim_value *= 0.98 + ((beatmap.overall_difficulty ** 2) / 2500)

    return aim_value


def get_speed_value(beatmap: Map, total_hits: int, misses: int, combo_reached: int, accuracy: float, num_50: int, mods: Mods = Mods.NM):
    speed_value = ((5 * max(1, beatmap.speed_difficulty / 0.0675) - 4) ** 3) / 100000

    length_bonus = 0.95 + 0.4 * min(1.0, total_hits / 2000) + (
        math.log10(total_hits / 2000) * 0.5 if total_hits > 2000 else 0)

    speed_value *= length_bonus

    if misses > 0:
        speed_value *= 0.97 * (1 - ((misses/total_hits) ** 0.775)) ** (misses ** 0.875)

    if beatmap.max_combo > 0:
        speed_value *= min((combo_reached ** 0.8) / (beatmap.max_combo ** 0.8), 1.0)

    approach_rate_factor = 0.0
    if beatmap.approach_rate > 10.33:
        approach_rate_factor += 0.4 * (beatmap.approach_rate - 10.33)

    speed_value *= 1 + min(approach_rate_factor, approach_rate_factor * (total_hits / 1000))

    if mods & Mods.HD:
        speed_value *= 1 + 0.04 * (12 - beatmap.approach_rate)

    speed_value *= (0.95 + ((beatmap.overall_difficulty ** 2) / 750)) * (accuracy ** ((14.5 - max(beatmap.overall_difficulty, 8.0)) / 2))
    speed_value *= 0.98 ** (0 if num_50 < total_hits / 500 else num_50 - total_hits / 500)

    return speed_value


def get_acc_value(beatmap: Map, total_hits: int, accuracy: float, num_300: int, num_100: int, num_50: int, mods: Mods = Mods.NM):
    better_acc_percentage, hit_objects_with_acc = 0, 0

    if mods & Mods.ScoreV2:
        better_acc_percentage = accuracy
        hit_objects_with_acc = total_hits
    else:
        hit_objects_with_acc = beatmap.circle_count
        if hit_objects_with_acc > 0:
            better_acc_percentage = ((num_300 - (total_hits - hit_objects_with_acc)) * 6 + num_100 * 2 + num_50) / (hit_objects_with_acc * 6)
        if better_acc_percentage < 0:
            better_acc_percentage = 0

    acc_value = (1.52163 ** beatmap.overall_difficulty) * (better_acc_percentage ** 24) * 2.83
    acc_value *= min(1.15, ((hit_objects_with_acc / 1000) ** 0.3))

    if mods & Mods.HD:
        acc_value *= 1.08

    if mods & Mods.FL:
        acc_value *= 1.02

    return acc_value
