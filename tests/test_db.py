import os
import pytest
from dotenv import load_dotenv
from pathlib import Path
import json

import osutools

load_dotenv()

token = os.environ["OSU_V1_TOKEN"]
is_github = os.environ["IS_GITHUB"]


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
