from types import SimpleNamespace
from threading import Thread, Condition
import arcade
import config
from mahjong.utils import parsing


# god is dead and this file killed him
_visual_context = None  # pylint: disable=C0103


class DrawableList(list):

    def draw(self):
        for elem in self:
            elem.draw()


class RectDrawable:

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def draw(self):
        arcade.draw_lrtb_rectangle_outline(*self.args, **self.kwargs)


class Visualizer(arcade.Window):

    def __init__(self):
        super().__init__(width=config.SCREEN_WIDTH, height=config.SCREEN_HEIGHT,
                         title=config.SCREEN_TITLE, update_rate=config.UPDATE_RATE)
        arcade.set_background_color(arcade.csscolor.DIM_GRAY)
        mock = arcade.Sprite(
            filename=config.TILE_IMAGES["front"], scale=config.TILE_SCALING)
        self.consts = SimpleNamespace(
            center_x=self.width // 2,
            center_y=self.height // 2,
            tile_width=mock.width,
            tile_height=mock.height)
        self.drawables = SimpleNamespace(scene=None, gui=None)
        self.gui_camera = None
        self.state = SimpleNamespace(
            bottom=self.__class__._default_player_state(),
            right=self.__class__._default_player_state(),
            top=self.__class__._default_player_state(),
            left=self.__class__._default_player_state(),
            dora_indicators=["blank"] * 5,
            round="East 1",
            tiles_remaining=35)
        self.need_update = False
        self._setup()

    @staticmethod
    def _default_player_state():
        return SimpleNamespace(
            points=30000,
            wind="East",
            discards=["blank"] * 15,
            hand=["blank"] * 14,
            draw="blank")

    def set_gamestate(self, gamestate):
        pstates = [self.state.bottom, self.state.right, self.state.top, self.state.left]
        for player, pstate in zip(gamestate.current_hand.players, pstates):
            pstate.points = player.points
            pstate.wind = str(player.seat).capitalize()
            pstate.discards = [str(tile) for tile in player.discards]
            sorted_hand = parsing.tileset_from_string(parsing.tileset_to_string(player.hand))
            pstate.hand = [str(tile) for tile in sorted_hand]
            pstate.draw = str(player.drawn_tile()) if player.drawn_tile() else None
        dora_indicators = [str(face) for face in gamestate.current_hand.wall.dora_indicators]
        ndora_revealed = gamestate.current_hand.wall.ndora_revealed
        unrevealed = ["back"] * (5 - ndora_revealed)
        self.state.dora_indicators = dora_indicators[:ndora_revealed] + unrevealed
        round_wind_str = str(gamestate.current_hand.round_wind).capitalize()
        self.state.round = f"{round_wind_str} {gamestate.current_hand.honba}"
        self.state.tiles_remaining = gamestate.current_hand.wall.remaining
        self.need_update = True

    def set_commands(self, commands):  # pylint: disable=W0613
        self.need_update = True  # TODO

    def get_command_batch(self):
        self.need_update = True  # TODO

    def on_update(self, delta_time):
        if self.need_update:
            self._remake_drawables()
            self.need_update = False

    def on_draw(self):
        self.clear()
        self.drawables.scene.draw()
        self._draw_gui()

    def _remake_drawables(self):
        self._clear_drawables()
        self._update_scene()
        self._update_gui()

    def _setup(self):
        self.drawables.scene = arcade.Scene()
        self.drawables.scene.add_sprite_list("tiles")
        self.drawables.gui = DrawableList()
        self.drawables.gui.append(arcade.Text("Loading...", self.consts.center_x,
            self.consts.center_y, color=arcade.csscolor.WHITE, font_size=30,
            anchor_x="center", anchor_y="center"))
        self.gui_camera = arcade.Camera(self.width, self.height)

    def _clear_drawables(self):
        self.drawables.scene.get_sprite_list("tiles").clear()
        self.drawables.gui.clear()

    def _add_tile(self, tile, rotation=0, **kwargs):
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
        self.drawables.scene.add_sprite("tiles", background)
        self.drawables.scene.add_sprite("tiles", face)

    def _add_tile_row(self, tiles, anchor_x=0, anchor_y=0, rotation=0, **kwargs):
        tile_half_width = self.consts.tile_width // 2
        tile_half_height = self.consts.tile_height // 2
        offset_x, offset_y = {
            0: (tile_half_width, -tile_half_height),
            90: (tile_half_height, tile_half_width),
            180: (-tile_half_width, tile_half_height),
            270: (-tile_half_height, -tile_half_width),
        }[rotation]
        stride = self.consts.tile_width + 2
        stride_x, stride_y = {0: (stride, 0), 90: (
            0, stride), 180: (-stride, 0), 270: (0, -stride)}[rotation]
        for i, tile in enumerate(tiles):
            self._add_tile(tile, center_x=anchor_x + offset_x + i * stride_x,
                           center_y=anchor_y + offset_y + i * stride_y, rotation=rotation, **kwargs)

    def _add_discard_pile(self, player, tiles):
        offset_x, offset_y, rotation = {
            "bottom": (103, 110, 0),
            "right": (-110, 103, 90),
            "top": (-103, -110, 180),
            "left": (110, -103, 270),
        }[player]
        row_offset = self.consts.tile_height + 2
        row_offset_x, row_offset_y = {"bottom": (0, row_offset), "right": (-row_offset, 0),
                                      "top": (0, -row_offset), "left": (row_offset, 0)}[player]
        self._add_tile_row(
            tiles[:6],
            anchor_x=self.consts.center_x - offset_x,
            anchor_y=self.consts.center_y - offset_y,
            rotation=rotation)
        self._add_tile_row(
            tiles[6:12],
            anchor_x=self.consts.center_x - offset_x - row_offset_x,
            anchor_y=self.consts.center_y - offset_y - row_offset_y,
            rotation=rotation)
        self._add_tile_row(
            tiles[12:],
            anchor_x=self.consts.center_x - offset_x - 2 * row_offset_x,
            anchor_y=self.consts.center_y - offset_y - 2 * row_offset_y,
            rotation=rotation)

    def _add_hand(self, player, tiles, draw=None):
        draw_offset = len(tiles) * (self.consts.tile_width + 2) + 10
        hand_offset = 4 * (self.consts.tile_width + 2)
        offset_x, offset_y, draw_offset_x, draw_offset_y, rotation = {
            "bottom": (103 + hand_offset, 330, draw_offset, 0, 0),
            "right": (-330, 103 + hand_offset, 0, draw_offset, 90),
            "top": (-103 - hand_offset, -330, -draw_offset, 0, 180),
            "left": (330, -103 - hand_offset, 0, -draw_offset, 270),
        }[player]
        anchor_x, anchor_y = self.consts.center_x -  offset_x, self.consts.center_y - offset_y
        self._add_tile_row(tiles[:13], anchor_x=anchor_x,
                           anchor_y=anchor_y, rotation=rotation)
        if draw:
            self._add_tile_row([draw], anchor_x=anchor_x + draw_offset_x,
                           anchor_y=anchor_y + draw_offset_y, rotation=rotation)

    def _add_dora_indicators(self, tiles):
        self._add_tile_row(tiles[:5], anchor_x=15, anchor_y=self.consts.tile_height + 15)

    def _update_scene(self):
        self._add_discard_pile("bottom", self.state.bottom.hand)
        self._add_discard_pile("right", self.state.right.hand)
        self._add_discard_pile("top", self.state.top.hand)
        self._add_discard_pile("left", self.state.left.hand)
        self._add_hand("bottom", self.state.bottom.hand, draw=self.state.bottom.draw)
        self._add_hand("right", self.state.right.hand, draw=self.state.right.draw)
        self._add_hand("top", self.state.top.hand, draw=self.state.top.draw)
        self._add_hand("left", self.state.left.hand, draw=self.state.left.draw)
        self._add_dora_indicators(self.state.dora_indicators)

    def _update_gui(self):
        gui = DrawableList()
        gui.append(arcade.Text(self.state.bottom.wind, self.consts.center_x - 90,
                               self.consts.center_y - 90, color=arcade.csscolor.WHITE,
                               rotation=0))
        gui.append(arcade.Text(self.state.right.wind, self.consts.center_x + 90,
                               self.consts.center_y - 90, color=arcade.csscolor.WHITE,
                               rotation=90))
        gui.append(arcade.Text(self.state.top.wind, self.consts.center_x + 90,
                               self.consts.center_y + 90, color=arcade.csscolor.WHITE,
                               rotation=180))
        gui.append(arcade.Text(self.state.left.wind, self.consts.center_x - 90,
                               self.consts.center_y + 90, color=arcade.csscolor.WHITE,
                               rotation=-90))
        gui.append(arcade.Text(str(self.state.bottom.points), self.consts.center_x,
                               self.consts.center_y - 60, color=arcade.csscolor.WHITE,
                                 rotation=0, font_size=18, anchor_x="center", anchor_y="center"))
        gui.append(arcade.Text(str(self.state.right.points), self.consts.center_x + 60,
                               self.consts.center_y, color=arcade.csscolor.WHITE,
                                 rotation=90, font_size=18, anchor_x="center", anchor_y="center"))
        gui.append(arcade.Text(str(self.state.top.points), self.consts.center_x,
                               self.consts.center_y + 60, color=arcade.csscolor.WHITE,
                               rotation=180, font_size=18, anchor_x="center", anchor_y="center"))
        gui.append(arcade.Text(str(self.state.left.points), self.consts.center_x - 60,
                               self.consts.center_y, color=arcade.csscolor.WHITE,
                               rotation=-90, font_size=18, anchor_x="center", anchor_y="center"))
        gui.append(arcade.Text(self.state.round, self.consts.center_x, self.consts.center_y + 15,
                               color=arcade.csscolor.WHITE, font_size=20, anchor_x="center",
                               anchor_y="center"))
        gui.append(arcade.Text(f"x{self.state.tiles_remaining}", self.consts.center_x,
                               self.consts.center_y - 15, color=arcade.csscolor.WHITE,
                               font_size=15, anchor_x="center", anchor_y="center"))
        gui.append(RectDrawable(self.consts.center_x - 100, self.consts.center_x + 100,
                                self.consts.center_y + 100, self.consts.center_y - 100,
                                arcade.csscolor.WHITE, border_width=3))
        self.drawables.gui.extend(gui)

    def _draw_gui(self):
        self.gui_camera.use()
        self.drawables.gui.draw()


def run_sync(condition):
    global _visual_context  # pylint: disable=C0103,W0603
    _visual_context = Visualizer()
    if condition:
        with condition:
            condition.notify()
    _visual_context.run()

def run():
    condition = Condition()
    if not _visual_context:
        Thread(target=run_sync, args=(condition,)).start()
    with condition:
        condition.wait()
    return _visual_context

# TODO remove later, just for quick and dirty debug
if __name__ == "__main__":
    visual_context = run()

    from mahjong.commands import CmdStartHand
    from mahjong import Engine, Wall, Meld, Mentsu, Seat
    seed = 0  # pylint: disable=C0103
    engine = Engine(seed=seed)
    CmdStartHand().execute(engine.gamestate)
    wall = Wall()
    wall.construct()
    ndiscards = [15, 17, 14, 14]
    for idx, p in enumerate(engine.gamestate.hands[-1].players):
        p.hand = [wall.draw() for _ in range(13)]
        p.discards = [wall.draw() for _ in range(ndiscards[idx])]
    engine.gamestate.hands[-1].players[0].hand.append(wall.draw())
    def nfromhand(hand, amount):
        return [hand.pop() for _ in range(amount)]
    ts = nfromhand(engine.gamestate.hands[-1].players[0].hand, 3)
    meld = Meld(variant=Mentsu.MINJUN, tiles=ts, called_tile=ts[0],
        called_player=engine.gamestate.hands[-1].get_player(Seat.EAST))
    engine.gamestate.hands[-1].players[0].called_melds.append(meld)
    ts = nfromhand(engine.gamestate.hands[-1].players[0].hand, 3)
    meld = Meld(variant=Mentsu.MINKOU, tiles=ts, called_tile=ts[1],
        called_player=engine.gamestate.hands[-1].get_player(Seat.SOUTH))
    engine.gamestate.hands[-1].players[0].called_melds.append(meld)
    ts = nfromhand(engine.gamestate.hands[-1].players[2].hand, 4)
    meld = Meld(variant=Mentsu.MINKAN, tiles=ts, called_tile=ts[2],
        called_player=engine.gamestate.hands[-1].get_player(Seat.WEST))
    engine.gamestate.hands[-1].players[2].called_melds.append(meld)
    ts = nfromhand(engine.gamestate.hands[-1].players[3].hand, 4)
    meld = Meld(variant=Mentsu.SHOUMINKAN, tiles=ts, called_tile=ts[3],
        called_player=engine.gamestate.hands[-1].get_player(Seat.NORTH))
    engine.gamestate.hands[-1].players[3].called_melds.append(meld)
    ts = nfromhand(engine.gamestate.hands[-1].players[3].hand, 4)
    meld = Meld(variant=Mentsu.ANKAN, tiles=ts)
    engine.gamestate.hands[-1].players[3].called_melds.append(meld)

    visual_context.set_gamestate(engine.gamestate)
