import datetime
import os
import pytest
from dotenv import load_dotenv
from pathlib import Path
import json

import osutools

load_dotenv()

token = os.environ["OSU_V1_TOKEN"]


@pytest.fixture(scope="module", autouse=True)
def load_client():
    client = osutools.OsuClientV1(token)
    path = Path("test_files") / "osu"
    client.set_osu_folder(path)
    yield client


def test_read_osu_db(load_client):
    assert load_client.osu_db.player_name == "flubb 4"
    assert load_client.osu_db.account_unlocked
    assert load_client.osu_db.number_of_beatmaps == len(load_client.osu_db.maps)


def test_search_local_maps(load_client):
    sofia = load_client.osu_db.search_maps("sofia")
    assert sofia and sofia[0].mapset_id == 1346543


def test_export_osu_db(load_client):
    json_path = "osu_db.json"
    load_client.osu_db.export(json_path)
    with open(json_path, "r") as f:
        osu_db = json.load(f)
    assert osu_db["player_name"] == "flubb 4"
    os.remove(json_path)


def test_read_collections_db(load_client):
    assert load_client.collections_db.no_collections == len(load_client.collections_db.collections)
    assert "0 stream warmup" in load_client.collections_db.collections.keys()


def test_export_collections(load_client):
    json_path = "collections_db.json"
    load_client.collections_db.export(json_path)
    with open(json_path, "r") as f:
        col_db = json.load(f)
    assert "0 stream warmup" in col_db["collections"].keys()
    os.remove(json_path)


def test_read_scores_db(load_client):
    score = load_client.scores_db.score_by_map[2788620][0]
    assert score.map_hash == "ab1a905e925901a2ed1228a998050037"
    assert score.username == "flubb 4"
    assert score.score == 4924176

    scores = load_client.scores_db.get_scores_before(datetime.datetime(year=2019, month=1, day=1, tzinfo=datetime.timezone.utc),
                                                  names=["flubb 4", "ito", "biglizard"], ranked_only=False)
    assert scores["9568062f1a47c504b94a29edcf2f60a9"][0].map.song_title == "Peace Sign (TV edit.)"
    assert scores["9568062f1a47c504b94a29edcf2f60a9"][0].score == 2817460
    assert scores["9568062f1a47c504b94a29edcf2f60a9"][0].username == "biglizard"
