import struct
# noinspection PyProtectedMember
from enum import Enum, Flag, _decompose  # yes this method is meant to be package private but Flag did everything I wanted it to apart from this
from datetime import timedelta, datetime, timezone


class Mode(Enum):
    """Translates api return to osu! gamemode"""
    STANDARD = 0
    TAIKO = 1
    CTB = 2
    MANIA = 3


class Teams(Enum):
    """Translates api return to osu! multiplayer team"""
    NONE = 0
    BLUE = 1
    RED = 2


class TeamType(Enum):
    """Translates api return to osu! multiplayer team type"""
    HEADTOHEAD = 0
    TAGCOOP = 1
    TEAMVS = 2
    TAGTEAMVS = 3


class WinCon(Enum):
    """Translates api return to osu! multiplayer scoring type"""
    SCORE = 0
    ACCURACY = 1
    COMBO = 2
    SCOREV2 = 3


class Approval(Enum):
    """Translates api return to a stage in the map ranking process"""
    GRAVEYARD = -2
    WIP = -1
    PENDING = 0
    RANKED = 1
    APPROVED = 2
    QUALIFIED = 3
    LOVED = 4


class Genre(Enum):
    """Translates an api return to a specific genre"""
    ANY = 0
    UNSPECIFIED = 1
    VIDEO_GAME = 2
    ANIME = 3
    ROCK = 4
    POP = 5
    OTHER = 6
    NOVELTY = 7
    HIP_HOP = 9
    ELECTRONIC = 10
    METAL = 11
    CLASSICAL = 12
    FOLK = 13
    JAZZ = 14


class Language(Enum):
    """Translates an api return to a specific language"""
    ANY = 0
    UNSPECIFIED = 1
    ENGLISH = 2
    JAPANESE = 3
    CHINESE = 4
    INSTRUMENTAL = 5
    KOREAN = 6
    FRENCH = 7
    GERMAN = 8
    SWEDISH = 9
    SPANISH = 10
    ITALIAN = 11
    RUSSIAN = 12
    POLISH = 13
    OTHER = 14


mod_order = ["EZ", "HD", "DT", "NC", "HT", "HR", "FL", "SD", "PF", "NF", "SO", "TF", "NM"]
"""[str]: Ordered list of mods. Can probably override to customise print order."""


# sorry alex
# noinspection PyProtectedMember
class Mods(Flag):
    """Translate between bitwise api return and mod combinations for a score """
    def __str__(self):
        """Represents the mod when it is printed

        Returns:
            str: string representing the mods used in the "correct" (up to interpretation but I used scoreposts as a base) order
        """
        m = self.mod_list()
        return ''.join([mod for mod in mod_order if mod in m])

    def mod_list(self):
        """Get a list of the mods used as strings

        Returns:
            [str]: mods used as strings names
        """
        members, uncovered = _decompose(self.__class__, self._value_)
        mods = [m._name_ for m in members]
        if "DT" in mods and "NC" in mods:
            mods.remove("DT")
        if "SD" in mods and "PF" in mods:
            mods.remove("SD")
        return mods

    NM = 0
    NF = 1
    EZ = 2
    TD = 4
    HD = 8
    HR = 16
    SD = 32
    DT = 64
    RX = 128
    HT = 256
    NC = 512  # Only set along with DoubleTime. i.e: NC only gives 576
    FL = 1024
    Autoplay = 2048
    SO = 4096
    Relax2 = 8192  # Autopilot
    PF = 16384  # Only set along with SuddenDeath. i.e: PF only gives 16416
    KEY4 = 32768
    KEY5 = 65536
    KEY6 = 131072
    KEY7 = 262144
    KEY8 = 524288
    FadeIn = 1048576
    Random = 2097152
    Cinema = 4194304
    Target = 8388608
    KEY9 = 16777216
    KEYCOOP = 33554432
    KEY1 = 67108864
    KEY3 = 134217728
    KEY2 = 268435456
    ScoreV2 = 536870912
    Mirror = 1073741824


def modstr_to_enums(mods: str):
    """Translate a string of mods into their respective enums

    Args:
        mods: string to parse

    Returns:
        [Mods]: list of mods used as enums
    """
    parsed_mods = []
    mods = mods.replace(" ", "")
    while mods:
        mod_str = ""
        for letter in mods:
            mod_str += letter
            try:
                parsed_mods.append(Mods[mod_str])
                break
            except KeyError:
                pass
        mods = mods[len(mod_str):]
    return parsed_mods


def parse_mod_string(mods: str):
    """Parse a mod string into one enum representing it.

    Args:
        mods: string of mods used (e.g. "HDDTHR")

    Returns:
        Mods: Mod enum representing the mod combination
    """
    return Mods(sum([x.value for x in modstr_to_enums(mods)]))


class Playtime:
    """Object holding some information about playtime. Can be printed to just show value.

    Attributes:
        seconds: seconds played
        hours: hours played
        days: days played
        combined: formatted time spent playing
    """
    def __init__(self, seconds):
        self.seconds = seconds
        self.hours = seconds / 60 / 60
        self.days = seconds / 60 / 60 / 24
        self.combined = timedelta(seconds=seconds)

    def __repr__(self):
        return f"{self.combined}"


def read_byte(db):
    return int.from_bytes(db.read(1), "little")


def read_short(db):
    return int.from_bytes(db.read(2), "little")


def read_int(db):
    data = db.read(4)
    return int.from_bytes(data, "little")


def read_long(db):
    return int.from_bytes(db.read(8), "little")


def read_single(db):
    return struct.unpack("<f", db.read(4))[0]


def read_double(db):
    return struct.unpack("<d", db.read(8))[0]


def read_bool(db):
    return struct.unpack("?", db.read(1))[0]


def read_leb128(db):
    result = 0
    shift = 0
    while True:
        byte = read_byte(db)
        result |= (byte & 0x7f) << shift
        if (byte & 0x80) == 0:
            break
        shift += 7
    return result


def read_string(db):
    present = db.read(1)
    if present == b'\x00':
        return None

    size = read_leb128(db)
    string = db.read(size)
    try:
        ret = string.decode('utf-8')
    except ValueError:
        ret = string.decode('ISO-8859-1')
    return ret


def read_int_double(db):
    fst = read_byte(db)
    item_1 = read_int(db)
    snd = read_byte(db)
    item_2 = read_double(db)
    return item_1, item_2


def read_timing(db):
    bpm = read_double(db)
    offset = read_double(db)
    inherited = read_bool(db)
    return bpm, offset, inherited


def read_datetime(db):
    ticks = read_long(db)
    start = datetime(year=2001, month=1, day=1, tzinfo=timezone.utc)
    return start + timedelta(microseconds=ticks*0.1)
