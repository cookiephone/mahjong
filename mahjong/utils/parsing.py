from collections import defaultdict
import re
from mahjong.tiles import Tile, Faces


STRING_MANZU = "m"
STRING_PINZU = "p"
STRING_SOUZU = "s"
STRING_HAKU = "W"
STRING_HATSU = "G"
STRING_CHUN = "R"
STRING_EAST = "e"
STRING_SOUTH = "s"
STRING_WEST = "w"
STRING_NORTH = "n"

ALL_TILES = (
    f"111122223333444405556666777788889999{STRING_MANZU}"
    f"111122223333444405556666777788889999{STRING_PINZU}"
    f"111122223333444405556666777788889999{STRING_SOUZU}"
    f"{STRING_HAKU * 4}{STRING_HATSU * 4}{STRING_CHUN * 4}"
    f"{STRING_EAST * 4}{STRING_SOUTH * 4}{STRING_WEST * 4}{STRING_NORTH * 4}"
)
ALL_TILES_NO_AKA = ALL_TILES.replace("0", "5")

PATTERN_MANZU = fr"\d+{STRING_MANZU}"
PATTERN_PINZU = fr"\d+{STRING_PINZU}"
PATTERN_SOUZU = fr"\d+{STRING_SOUZU}"
PATTERN_MPS = f"{PATTERN_MANZU}|{PATTERN_PINZU}|{PATTERN_SOUZU}"
PATTERN_HAKU = f"{STRING_HAKU}"
PATTERN_HATSU = f"{STRING_HATSU}"
PATTERN_CHUN = f"{STRING_CHUN}"
PATTERN_DRAGON = f"{PATTERN_HAKU}|{PATTERN_HATSU}|{PATTERN_CHUN}"
PATTERN_EAST = f"{STRING_EAST}"
PATTERN_SOUTH = f"{STRING_SOUTH}"
PATTERN_WEST = f"{STRING_WEST}"
PATTERN_NORTH = f"{STRING_NORTH}"
PATTERN_WIND = f"{PATTERN_EAST}|{PATTERN_SOUTH}|{PATTERN_WEST}|{PATTERN_NORTH}"
PATTERN_TILESET = f"(?:{PATTERN_MPS}|{PATTERN_DRAGON}|{PATTERN_WIND})*"

DIGIT_ORDER = [1, 2, 3, 4, 0, 5, 6, 7, 8, 9]
HONOR_ORDER = [STRING_HAKU, STRING_HATSU, STRING_CHUN,
               STRING_EAST, STRING_SOUTH, STRING_WEST, STRING_NORTH]

LUT_DIGIT_MANZU = {
    0: Faces.MAN5_AKA,
    1: Faces.MAN1,
    2: Faces.MAN2,
    3: Faces.MAN3,
    4: Faces.MAN4,
    5: Faces.MAN5,
    6: Faces.MAN6,
    7: Faces.MAN7,
    8: Faces.MAN8,
    9: Faces.MAN9,
}
LUT_MANZU_DIGIT = {v: k for k, v in LUT_DIGIT_MANZU.items()}

LUT_DIGIT_PINZU = {
    0: Faces.PIN5_AKA,
    1: Faces.PIN1,
    2: Faces.PIN2,
    3: Faces.PIN3,
    4: Faces.PIN4,
    5: Faces.PIN5,
    6: Faces.PIN6,
    7: Faces.PIN7,
    8: Faces.PIN8,
    9: Faces.PIN9,
}
LUT_PINZU_DIGIT = {v: k for k, v in LUT_DIGIT_PINZU.items()}

LUT_DIGIT_SOUZU = {
    0: Faces.SOU5_AKA,
    1: Faces.SOU1,
    2: Faces.SOU2,
    3: Faces.SOU3,
    4: Faces.SOU4,
    5: Faces.SOU5,
    6: Faces.SOU6,
    7: Faces.SOU7,
    8: Faces.SOU8,
    9: Faces.SOU9,
}
LUT_SOUZU_DIGIT = {v: k for k, v in LUT_DIGIT_SOUZU.items()}


class TilesetStringNotSaneException(Exception):
    pass


def _tileset_string_sanity(string):
    pattern = re.compile(PATTERN_TILESET)
    match = re.fullmatch(pattern, string)
    return match is not None


def _digits_from_match(match):
    matchstring = "".join(match)
    digitmatch = re.findall(re.compile(r"\d+"), matchstring)
    digitstring = "".join(digitmatch)
    digits = [int(d) for d in digitstring]
    digits.sort(key=DIGIT_ORDER.index)
    return digits


def tileset_from_string(string):
    if not _tileset_string_sanity(string):
        raise TilesetStringNotSaneException(
            f"string '{string}' does not fully match pattern {PATTERN_TILESET}")
    manzu = _digits_from_match(re.findall(re.compile(PATTERN_MANZU), string))
    pinzu = _digits_from_match(re.findall(re.compile(PATTERN_PINZU), string))
    souzu = _digits_from_match(re.findall(re.compile(PATTERN_SOUZU), string))
    nhaku = len(re.findall(re.compile(PATTERN_HAKU), string))
    nhatsu = len(re.findall(re.compile(PATTERN_HATSU), string))
    nchun = len(re.findall(re.compile(PATTERN_CHUN), string))
    neast = len(re.findall(re.compile(PATTERN_EAST), string))
    nsouth = len(re.findall(re.compile(PATTERN_SOUTH), string))
    nwest = len(re.findall(re.compile(PATTERN_WEST), string))
    nnorth = len(re.findall(re.compile(PATTERN_NORTH), string))
    tiles = []
    tiles.extend([Tile(face=LUT_DIGIT_MANZU[d]) for d in manzu])
    tiles.extend([Tile(face=LUT_DIGIT_PINZU[d]) for d in pinzu])
    tiles.extend([Tile(face=LUT_DIGIT_SOUZU[d]) for d in souzu])
    tiles.extend([Tile(face=Faces.HAKU) for _ in range(nhaku)])
    tiles.extend([Tile(face=Faces.HATSU) for _ in range(nhatsu)])
    tiles.extend([Tile(face=Faces.CHUN) for _ in range(nchun)])
    tiles.extend([Tile(face=Faces.EAST) for _ in range(neast)])
    tiles.extend([Tile(face=Faces.SOUTH) for _ in range(nsouth)])
    tiles.extend([Tile(face=Faces.WEST) for _ in range(nwest)])
    tiles.extend([Tile(face=Faces.NORTH) for _ in range(nnorth)])
    return tiles


def tileset_to_string(tiles):
    nface = defaultdict(lambda: 0)
    mpsdigits = defaultdict(lambda: [])
    for tile in tiles:
        match tile:
            case Tile(face=Faces.HAKU):
                nface[STRING_HAKU] += 1
            case Tile(face=Faces.HATSU):
                nface[STRING_HATSU] += 1
            case Tile(face=Faces.CHUN):
                nface[STRING_CHUN] += 1
            case Tile(face=Faces.EAST):
                nface[STRING_EAST] += 1
            case Tile(face=Faces.SOUTH):
                nface[STRING_SOUTH] += 1
            case Tile(face=Faces.WEST):
                nface[STRING_WEST] += 1
            case Tile(face=Faces.NORTH):
                nface[STRING_NORTH] += 1
            case Tile(face=face) if face in Faces.MANZU:
                mpsdigits[STRING_MANZU].append(LUT_MANZU_DIGIT[face])
            case Tile(face=face) if face in Faces.PINZU:
                mpsdigits[STRING_PINZU].append(LUT_PINZU_DIGIT[face])
            case Tile(face=face) if face in Faces.SOUZU:
                mpsdigits[STRING_SOUZU].append(LUT_SOUZU_DIGIT[face])
    mpsdigits[STRING_MANZU].sort(key=DIGIT_ORDER.index)
    mpsdigits[STRING_PINZU].sort(key=DIGIT_ORDER.index)
    mpsdigits[STRING_SOUZU].sort(key=DIGIT_ORDER.index)
    mpsdigits[STRING_MANZU] = map(str, mpsdigits[STRING_MANZU])
    mpsdigits[STRING_PINZU] = map(str, mpsdigits[STRING_PINZU])
    mpsdigits[STRING_SOUZU] = map(str, mpsdigits[STRING_SOUZU])
    string = ""
    string += f"{''.join(mpsdigits[STRING_MANZU])}{STRING_MANZU}" if mpsdigits[STRING_MANZU] else ""
    string += f"{''.join(mpsdigits[STRING_PINZU])}{STRING_PINZU}" if mpsdigits[STRING_PINZU] else ""
    string += f"{''.join(mpsdigits[STRING_SOUZU])}{STRING_SOUZU}" if mpsdigits[STRING_SOUZU] else ""
    for honorstring in HONOR_ORDER:
        string += honorstring * nface[honorstring]
    return string
