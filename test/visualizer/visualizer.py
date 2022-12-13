import arcade
import config


# god is dead and this code is what killed him
class Visualizer(arcade.Window):

    def __init__(self):
        super().__init__(width=config.SCREEN_WIDTH, height=config.SCREEN_HEIGHT,
                         title=config.SCREEN_TITLE, update_rate=config.UPDATE_RATE)
        self.center_x = self.width // 2
        self.center_y = self.height // 2
        mock = arcade.Sprite(
            filename=config.TILE_IMAGES["front"], scale=config.TILE_SCALING)
        self.tile_width = mock.width
        self.tile_height = mock.height
        arcade.set_background_color(arcade.csscolor.DIM_GRAY)
        self.scene = None
        self.texts = None
        self.gui_camera = None

    def setup(self):
        self.scene = arcade.Scene()
        self.scene.add_sprite_list("tiles")
        self.texts = []
        self.gui_camera = arcade.Camera(self.width, self.height)

    def on_update(self, delta_time):
        self.update_scene()
        self.update_gui()

    def on_draw(self):
        self.clear()
        self.scene.draw()
        self.draw_gui()

    def add_tile(self, tile, rotation=0, **kwargs):
        background = arcade.Sprite(
            **kwargs | {
                "angle": rotation,
                "filename": config.TILE_IMAGES["front"],
                "scale": config.TILE_SCALING})
        face = arcade.Sprite(
            **kwargs | {
                "angle": rotation,
                "filename": config.TILE_IMAGES[tile],
                "scale": config.TILE_SCALING})
        self.scene.add_sprite("tiles", background)
        self.scene.add_sprite("tiles", face)

    def add_tile_row(self, tiles, anchor_x=0, anchor_y=0, rotation=0, **kwargs):
        tile_half_width, tile_half_height = self.tile_width // 2, self.tile_height // 2
        offset_x, offset_y = {
            0: (tile_half_width, -tile_half_height),
            90: (tile_half_height, tile_half_width),
            180: (-tile_half_width, tile_half_height),
            270: (-tile_half_height, -tile_half_width),
        }[rotation]
        stride = self.tile_width + 2
        stride_x, stride_y = {0: (stride, 0), 90: (
            0, stride), 180: (-stride, 0), 270: (0, -stride)}[rotation]
        for i, tile in enumerate(tiles):
            self.add_tile(tile, center_x=anchor_x + offset_x + i * stride_x,
                          center_y=anchor_y + offset_y + i * stride_y, rotation=rotation, **kwargs)

    def add_discard_pile(self, player, tiles):
        offset_x, offset_y, rotation = {
            "bottom": (103, 110, 0),
            "right": (-110, 103, 90),
            "top": (-103, -110, 180),
            "left": (110, -103, 270),
        }[player]
        row_offset = self.tile_height + 2
        row_offset_x, row_offset_y = {"bottom": (0, row_offset), "right": (-row_offset, 0),
                                      "top": (0, -row_offset), "left": (row_offset, 0)}[player]
        self.add_tile_row(
            tiles[:6],
            anchor_x=self.center_x - offset_x,
            anchor_y=self.center_y - offset_y,
            rotation=rotation)
        self.add_tile_row(
            tiles[6:12],
            anchor_x=self.center_x - offset_x - row_offset_x,
            anchor_y=self.center_y - offset_y - row_offset_y,
            rotation=rotation)
        self.add_tile_row(
            tiles[12:],
            anchor_x=self.center_x - offset_x - 2 * row_offset_x,
            anchor_y=self.center_y - offset_y - 2 * row_offset_y,
            rotation=rotation)

    def add_hand(self, player, tiles, draw=None):
        draw_offset = 13 * (self.tile_width + 2) + 10
        hand_offset = 4 * (self.tile_width + 2)
        offset_x, offset_y, draw_offset_x, draw_offset_y, rotation = {
            "bottom": (103 + hand_offset, 330, draw_offset, 0, 0),
            "right": (-330, 103 + hand_offset, 0, draw_offset, 90),
            "top": (-103 - hand_offset, -330, -draw_offset, 0, 180),
            "left": (330, -103 - hand_offset, 0, -draw_offset, 270),
        }[player]
        anchor_x, anchor_y = self.center_x - offset_x, self.center_y - offset_y
        self.add_tile_row(tiles[:13], anchor_x=anchor_x,
                          anchor_y=anchor_y, rotation=rotation)
        if draw:
            self.add_tile_row([draw], anchor_x=anchor_x + draw_offset_x,
                              anchor_y=anchor_y + draw_offset_y, rotation=rotation)

    def add_dora_indicators(self, tiles):
        self.add_tile_row(tiles[:5], anchor_x=15,
                          anchor_y=self.tile_height + 15)

    def update_scene(self):
        self.add_discard_pile("bottom", ["haku"] * 15)
        self.add_discard_pile("right", ["haku"] * 15)
        self.add_discard_pile("top", ["haku"] * 15)
        self.add_discard_pile("left", ["haku"] * 15)
        self.add_hand("bottom", ["haku"] * 13, draw="haku")
        self.add_hand("right", ["haku"] * 13, draw="haku")
        self.add_hand("top", ["haku"] * 13, draw="haku")
        self.add_hand("left", ["haku"] * 13, draw="haku")
        self.add_dora_indicators(["haku", "back", "back", "back", "back"])

    def update_gui(self):
        self.texts = []
        self.texts.append(arcade.Text("East", self.center_x - 90,
                          self.center_y - 90, color=arcade.csscolor.WHITE, rotation=0))
        self.texts.append(arcade.Text("South", self.center_x + 90,
                          self.center_y - 90, color=arcade.csscolor.WHITE, rotation=90))
        self.texts.append(arcade.Text("West", self.center_x + 90,
                          self.center_y + 90, color=arcade.csscolor.WHITE, rotation=180))
        self.texts.append(arcade.Text("North", self.center_x - 90,
                          self.center_y + 90, color=arcade.csscolor.WHITE, rotation=-90))
        self.texts.append(arcade.Text("30000", self.center_x, self.center_y - 60,
                          color=arcade.csscolor.WHITE, rotation=0, font_size=18,
                          anchor_x="center", anchor_y="center"))
        self.texts.append(arcade.Text("30000", self.center_x + 60, self.center_y,
                          color=arcade.csscolor.WHITE, rotation=90, font_size=18,
                          anchor_x="center", anchor_y="center"))
        self.texts.append(arcade.Text("30000", self.center_x, self.center_y + 60,
                          color=arcade.csscolor.WHITE, rotation=180, font_size=18,
                          anchor_x="center", anchor_y="center"))
        self.texts.append(arcade.Text("30000", self.center_x - 60, self.center_y,
                          color=arcade.csscolor.WHITE, rotation=-90, font_size=18,
                          anchor_x="center", anchor_y="center"))
        self.texts.append(arcade.Text("East 1", self.center_x, self.center_y + 15,
                          color=arcade.csscolor.WHITE, font_size=20,
                          anchor_x="center", anchor_y="center"))
        self.texts.append(arcade.Text("x35", self.center_x, self.center_y - 15,
                          color=arcade.csscolor.WHITE, font_size=15,
                          anchor_x="center", anchor_y="center"))

    def draw_gui(self):
        self.gui_camera.use()
        arcade.draw_lrtb_rectangle_outline(self.center_x - 100, self.center_x + 100,
                                           self.center_y + 100, self.center_y - 100,
                                           arcade.csscolor.WHITE, border_width=3)
        for text in self.texts:
            text.draw()


def run():
    window = Visualizer()
    window.setup()
    arcade.run()


# TODO remove later
if __name__ == "__main__":
    run()
