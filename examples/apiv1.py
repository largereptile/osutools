import osutools

osu = osutools.OsuClient("token")

# Get user
me = osu.fetch_user(username="flubb 4")
print(f"{me} | {me.pp}pp | #{me.rank} Global")

# Get best 5 scores
best = me.fetch_best()[:5]

# Show information about scores
for score in best:
    beatmap = score.fetch_map()
    print(f"{score.pp}pp | {score.score} | {beatmap} | {score.mods}")

# Get information about a specific beatmap
beatmap = osu.fetch_map(map_id=2788620)
print(f"{beatmap.song_title} [{beatmap.difficulty_name}] | {beatmap.artist} | {beatmap.creator_name}")

# Get leaderboards and submitted scores for the beatmap
leaderboard = beatmap.fetch_scores()
my_score = beatmap.fetch_scores(username="flubb 4")[0]
print(f"Best Score: {leaderboard[0]}\nMy Score: {my_score}")
