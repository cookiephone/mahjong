from pathlib import Path
import arcade


SCREEN_WIDTH = 1100
SCREEN_HEIGHT = 900
SCREEN_TITLE = "Riichi Mahjong Visualizer"
TILE_SCALING = 0.054
UPDATE_RATE = 1 / 60

BUTTON_STYLE = {
    "bg_color": arcade.color.EERIE_BLACK,
    "bg_color_pressed": arcade.color.LIGHT_GRAY,
    "bg_color_hovered": arcade.color.JET,
    "bg_color_disabled": arcade.color.DARK_GRAY,
    "border_color": None,
    "border_color_pressed": arcade.color.WHITE,
    "border_color_hovered": None,
    "border_color_disabled": None,
    "font_size": 11,
}

RESOURCES_PATH = Path(__file__).parent / "resources"
TILE_IMAGES = {
    "back": RESOURCES_PATH / "tiles/Back.png",
    "blank": RESOURCES_PATH / "tiles/Blank.png",
    "front": RESOURCES_PATH / "tiles/Front.png",
    "chun": RESOURCES_PATH / "tiles/Chun.png",
    "haku": RESOURCES_PATH / "tiles/Haku.png",
    "hatsu": RESOURCES_PATH / "tiles/Hatsu.png",
    "south": RESOURCES_PATH / "tiles/Nan.png",
    "north": RESOURCES_PATH / "tiles/Pei.png",
    "west": RESOURCES_PATH / "tiles/Shaa.png",
    "east": RESOURCES_PATH / "tiles/Ton.png",
    "1 man": RESOURCES_PATH / "tiles/Man1.png",
    "2 man": RESOURCES_PATH / "tiles/Man2.png",
    "3 man": RESOURCES_PATH / "tiles/Man3.png",
    "4 man": RESOURCES_PATH / "tiles/Man4.png",
    "5 man": RESOURCES_PATH / "tiles/Man5.png",
    "5 man aka": RESOURCES_PATH / "tiles/Man5-Dora.png",
    "6 man": RESOURCES_PATH / "tiles/Man6.png",
    "7 man": RESOURCES_PATH / "tiles/Man7.png",
    "8 man": RESOURCES_PATH / "tiles/Man8.png",
    "9 man": RESOURCES_PATH / "tiles/Man9.png",
    "1 pin": RESOURCES_PATH / "tiles/Pin1.png",
    "2 pin": RESOURCES_PATH / "tiles/Pin2.png",
    "3 pin": RESOURCES_PATH / "tiles/Pin3.png",
    "4 pin": RESOURCES_PATH / "tiles/Pin4.png",
    "5 pin": RESOURCES_PATH / "tiles/Pin5.png",
    "5 pin aka": RESOURCES_PATH / "tiles/Pin5-Dora.png",
    "6 pin": RESOURCES_PATH / "tiles/Pin6.png",
    "7 pin": RESOURCES_PATH / "tiles/Pin7.png",
    "8 pin": RESOURCES_PATH / "tiles/Pin8.png",
    "9 pin": RESOURCES_PATH / "tiles/Pin9.png",
    "1 sou": RESOURCES_PATH / "tiles/Sou1.png",
    "2 sou": RESOURCES_PATH / "tiles/Sou2.png",
    "3 sou": RESOURCES_PATH / "tiles/Sou3.png",
    "4 sou": RESOURCES_PATH / "tiles/Sou4.png",
    "5 sou": RESOURCES_PATH / "tiles/Sou5.png",
    "5 sou aka": RESOURCES_PATH / "tiles/Sou5-Dora.png",
    "6 sou": RESOURCES_PATH / "tiles/Sou6.png",
    "7 sou": RESOURCES_PATH / "tiles/Sou7.png",
    "8 sou": RESOURCES_PATH / "tiles/Sou8.png",
    "9 sou": RESOURCES_PATH / "tiles/Sou9.png",
}
