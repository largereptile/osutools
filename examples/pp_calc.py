import osutools
from osutools.utils import Mods
from osutools.oppai import Oppai

osu = osutools.OsuClient("token")

beatmap_path = "96neko - Uso no Hibana (Enjoy) [Hanabi].osu"
mod_combo = Mods.HR & Mods.HD
pp = Oppai.calculate_pp(beatmap_path, mods=mod_combo.value, accuracy=97.0)
print(pp)

beatmap = osu.fetch_map(1255495)
pp = Oppai.calculate_pp_from_url(beatmap.download_url, mods=mod_combo.value, accuracy=99.5)
print(pp)

