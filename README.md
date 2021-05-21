# osu!-tools for python

[![GitHub license](https://img.shields.io/github/license/largereptile/osutools)](https://github.com/largereptile/osutools/blob/main/LICENSE.md)
[![GitHub stars](https://img.shields.io/github/stars/largereptile/osutools)](https://github.com/largereptile/osutools/stargazers)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/osu-tools)](https://pypi.org/project/osu-tools/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/osu-tools)](https://pypi.org/project/osu-tools/)

## Description
osu!-tools is a Python framework for interacting with various osu! APIs and file-types.
- Make requests to the osu! v1 API to view user, score, map or match information.
- Uses oppai-ng to get pp information for any given score
- Read osu!.db, scores.db and collection.db into a Python object, and export it to json (export not actually implemented yet)

## Installation
```bash
pip install osu-tools
```

## Basic Examples
### Setup
```python console
>> import osutools

# Authenticate a client using an osu! API token
>> osu = osutools.OsuClient("token")
```

### API v1
- Get User
```python console
>> me = osu.fetch_user(username="flubb 4")
>> print(f"{me} | {me.pp}pp | #{me.rank} Global")

flubb 4 | 7507.3pp | #8765 Global
```

- Get best 5 scores + show information
```python console
>> best = me.fetch_best()[:5]


>> for score in best:
..  beatmap = score.fetch_map()
..  print(f"{score.pp}pp | {score.score} | {beatmap} | {score.mods}")

431.448pp | 1554216 | WONDERFUL WONDER (TV Size) [Simple Heart] mapped by Kuki1537 | DT
399.029pp | 44559304 | Flames Within These Black Feathers [Kowari's Extreme] mapped by Seni | NM
387.581pp | 2219153 | Angel With A Shotgun (Sped Up Ver.) [Sacred Bullet] mapped by Sotarks | HDDT
379.095pp | 377539970 | Save Me [Tragedy] mapped by Drummer | NM
371.206pp | 6547546 | One by One [Sotarks' Rampage] mapped by Elinor | HR
```

- Get information about a specific beatmap
```python console
>> beatmap = osu.fetch_map(map_id=2788620)
>> print(f"{beatmap.song_title} [{beatmap.difficulty_name}] | {beatmap.artist} | {beatmap.creator_name}")

Sofia [Nyantiaz's Hard] | Clairo | Qiyana
```

- Get leaderboards and submitted scores for the beatmap
```python console
>> leaderboard = beatmap.fetch_scores()
>> my_score = beatmap.fetch_scores(username="flubb 4")[0]
>> print(f"Best Score: {leaderboard[0]}\nMy Score: {my_score}")

Best Score: HDDTHR score on beatmap 2788620 by Mikayla
My Score: HDDT score on beatmap 2788620 by flubb 4
```

### Databases
- Set osu directory, and automatically read the databases.
```python console
>> osu.set_osu_folder("path/to/folder")

# Load the pp values for all local plays (enables faster processing of functions that use the pp value like get_best_scores_before()
>> osu.scores_db.load_pp()
```

- Get the average length of all of your maps
```python console
>> avg_map_length = sum([beatmap.length for beatmap in osu.osu_db.map_list()]) / float(len(osu.osu_db.map_list()))
>> print(timedelta(milliseconds=avg_map_length))

0:02:35.320889
```

- Get your top 10 ranked scores before 2020
```python console
>> names = ["flubb 4", "ito", "biglizard"] # I've changed my username a lot
>> scores = osu.scores_db.get_best_scores_before(datetime.datetime(year=2020, month=1, day=1, tzinfo=timezone.utc), names=, ranked_only=True)
>> for x, score in enumerate(scores[:5]):
..    print(f"{x+1}: {score.pp} play on {score.map.song_title} [{score.map.difficulty_name}] with {score.mods}")

1: 312.0760803222656 play on Snow Halation (feat. BeasttrollMC) [Reform's Extra] with DT
2: 311.7738952636719 play on Harumachi Clover (Swing Arrangement) [Dictate Edit] [Expert] with DT
3: 277.50250244140625 play on Yuki no Hana [Sharlo's Insane] with DT
4: 272.4308776855469 play on Kira Kira Days [Shiawase!!] with NM
5: 269.6291198730469 play on Natsukoi Hanabi [Insane] with DT
```

- Export your databases to JSON
```python console
>> osu.osu_db.export() # saves to osu_db.json by default
>> osu.scores_db.export("~/osu/scores.json") # can give custom path
```

### PP Calculation
- Get pp for an SS on a given map with HDHR
```python console
>> from osutools.utils import Mods
>> from osutools.oppai import Oppai

>> beatmap_path = "96neko - Uso no Hibana (Enjoy) [Hanabi].osu"
>> mod_combo = Mods.HR & Mods.HD
>> pp = Oppai.calculate_pp(beatmap_path, mods=mod_combo.value)
>> print(pp)

219.83245849609375
```

## Acknowledgements
- https://github.com/Francesco149/oppai-ng for the PP calculation, I just used ctypes to make it python
