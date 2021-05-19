# osu!-tools for python

## Description
osu!-tools is a Python framework for interacting with various osu! APIs and file-types.
- Make requests to the osu! v1 API to view user, score, map or match information.
- Uses pyttanko to get pp information for any given score
- Read osu!.db, scores.db and collection.db into a Python object, and export it to json (export not actually implemented yet)

## Basic Examples
### API v1
```python
import osutools

# Authenticate a client using an osu! API token
osu = osutools.OsuClient("token")

# Get user
me = osu.fetch_user(username="flubb 4")
print(f"{me} | {me.pp}pp | #{me.rank} Global")
flubb 4 | 7507.3pp | #8765 Global
```

```python
# Get best 5 scores
best = me.fetch_best()[:5]

# Show information about scores
for score in best:
    beatmap = score.fetch_map()
    print(f"{score.pp}pp | {score.score} | {beatmap} | {score.mods}")
431.448pp | 1554216 | WONDERFUL WONDER (TV Size) [Simple Heart] mapped by Kuki1537 | DT
399.029pp | 44559304 | Flames Within These Black Feathers [Kowari's Extreme] mapped by Seni | NM
387.581pp | 2219153 | Angel With A Shotgun (Sped Up Ver.) [Sacred Bullet] mapped by Sotarks | HDDT
379.095pp | 377539970 | Save Me [Tragedy] mapped by Drummer | NM
371.206pp | 6547546 | One by One [Sotarks' Rampage] mapped by Elinor | HR
```

```python
# Get information about a specific beatmap
beatmap = osu.fetch_map(map_id=2788620)
print(f"{beatmap.song_title} [{beatmap.difficulty_name}] | {beatmap.artist} | {beatmap.creator_name}")
Sofia [Nyantiaz's Hard] | Clairo | Qiyana
```

```python
# Get leaderboards and submitted scores for the beatmap
leaderboard = beatmap.fetch_scores()
my_score = beatmap.fetch_scores(username="flubb 4")[0]
print(f"Best Score: {leaderboard[0]}\nMy Score: {my_score}")
Best Score: HDDTHR score on beatmap 2788620 by Mikayla
My Score: HDDT score on beatmap 2788620 by flubb 4
```