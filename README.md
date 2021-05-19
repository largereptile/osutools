# osu!-tools for python

## Description
osu!-tools is a Python framework for interacting with various osu! APIs and file-types.
- Make requests to the osu! v1 API to view user, score, map or match information.
- Uses pyttanko to get pp information for any given score
- Read osu!.db, scores.db and collection.db into a Python object, and export it to json (export not actually implemented yet)

## Example Usage
### API v1
```pycon
import osutools
from osutools.utils import Mods

# Authenticate a client using an osu! API token
>> osu = osutools.OsuClient("token")

# Get information about a specific user
>> me = osu.fetch_user(username="flubb 4")
flubb 4
# Get that user's best scores
>> me.fetch_best()

# Get all "recent" plays since the last time this function was called
>> new_recent = me.fetch_new_recent()

# Get information about a beatmap
>> beatmap = osu.fetch_map(map_id=2788620)

# Get top 50 scores on that map
>> scores = beatmap.fetch_scores()

# Get a specific score from that map
>> my_score = beatmap.fetch_scores(username="flubb 4", mods=(Mods.DT & Mods.HD))[0]

# Get info about pp for the map
>> pp = beatmap.get_pp(mods=(Mods.DT & Mods.HR & Mods.HD))

```