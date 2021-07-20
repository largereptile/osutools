import os
import pytest
from dotenv import load_dotenv
import datetime

import osutools

load_dotenv()

token = os.environ["OSU_V1_TOKEN"]


@pytest.fixture(scope="module", autouse=True)
def load_client():
    client = osutools.OsuClient(token)
    yield client


def test_fetch_user(load_client):
    user = load_client.fetch_user(user_id=11903239)
    assert user.username == "flubb 4"


def test_fetch_scores(load_client):
    scores = load_client.fetch_scores(map_id=2413216, user_id=11903239)
    scores = list(map(lambda x: x.score, scores))
    assert 44559304 in scores


def test_fetch_map(load_client):
    beatmap = load_client.fetch_map(2413216)
    assert beatmap.song_title == "Flames Within These Black Feathers"


def test_fetch_maps(load_client):
    maps = load_client.fetch_maps(1001825)
    maps = set(map(lambda x: x.song_title, maps))
    assert maps == {"Flames Within These Black Feathers"}


def test_fetch_user_best(load_client):
    scores = load_client.fetch_user_best(user_id=11903239)
    last_pp = 5000
    for score in scores:
        assert score.pp < last_pp
        last_pp = score.pp


def test_fetch_user_recent(load_client):
    scores = load_client.fetch_user_recent(user_id=11903239)
    for score in scores:
        assert score.timestamp > (datetime.datetime.now() - datetime.timedelta(days=1))
