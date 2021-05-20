import osutools
import datetime
from datetime import timezone, timedelta

osu = osutools.OsuClient("token")

# Set osu directory, and automatically read the databases.
osu.set_osu_folder("C:\\Users\\harry\\AppData\\Local\\osu!")

# Load the pp values for all local plays (enables faster processing of functions that use the pp value like get_best_scores_before()
osu.scores_db.load_pp()

# Get the average length of all of your maps
avg_map_length = sum([beatmap.length for beatmap in osu.osu_db.map_list()]) / float(len(osu.osu_db.map_list()))
print(timedelta(milliseconds=avg_map_length))

# Get all top 100 ranked scores before 2020 and print
scores = osu.scores_db.get_best_scores_before(datetime.datetime(year=2019, month=6, day=1, tzinfo=timezone.utc), names=["flubb 4", "ito", "biglizard"], ranked_only=False)
for x, score in enumerate(scores[:5]):
    print(f"{x+1}: {score.pp} play on {score.map.song_title} [{score.map.difficulty_name}] with {score.mods}")

