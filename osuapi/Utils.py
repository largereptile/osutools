from enum import Enum, Flag
from datetime import timedelta


class Mode(Enum):
    STANDARD = 0
    TAIKO = 1
    CTB = 2
    MANIA = 3


class Approval(Enum):
    GRAVEYARD = -2
    WIP = -1
    PENDING = 0
    RANKED = 1
    APPROVED = 2
    QUALIFIED = 3
    LOVED = 4


class Genre(Enum):
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


class Mods(Flag):
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
    Autotap = 2048
    SO = 4096
    Autopilot = 8192
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


class Playtime:
    def __init__(self, seconds):
        self.seconds = seconds
        self.hours = seconds / 60 / 60
        self.days = seconds / 60 / 60 / 24
        self.combined = timedelta(seconds=seconds)

    def __repr__(self):
        return f"{self.combined}"
