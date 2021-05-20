import osutools
from osutools.utils import Mods

beatmap_path = "96neko - Uso no Hibana (Enjoy) [Hanabi].osu"
mod_combo = Mods.HR & Mods.HD
pp = osutools.Oppai.calculate_pp(beatmap_path, mods=mod_combo.value)
print(pp)
