from pathlib import Path

from osutools.oppai import Oppai


def test_calculate_pp():
    pp = Oppai.calculate_pp(
        Path("test_files")
        / "osu"
        / "Songs"
        / "559978 96neko - Uso no Hibana"
        / "96neko - Uso no Hibana (Enjoy) [Hanabi].osu",
        max_combo=529,
        num_50=1,
        num_100=39,
    )
    # live is 150 apparently so I'll just leave this as a boundary
    assert 140 < pp < 160


def test_calculate_from_url():
    beatmap_url = "https://osu.ppy.sh/osu/2413216"
    pp = Oppai.calculate_pp_from_url(url=beatmap_url, max_combo=1571, accuracy=99.32)
    assert 390 < pp < 410
