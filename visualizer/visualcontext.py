from types import SimpleNamespace
from threading import Thread, Condition
import arcade
import arcade.gui
import config
from button import Button
from drawablelist import DrawableList
from rectdrawable import RectDrawable
from mahjong.utils import parsing


# god is dead and this file killed him
_visual_context = None  # pylint: disable=C0103


class VisualContext(arcade.Window):

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
        self.drawables = SimpleNamespace(scene=None, gui=None, buttons=None)
        self.gui_camera = None
        self.state = SimpleNamespace(
            bottom=self.__class__._default_player_state(),
            right=self.__class__._default_player_state(),
            top=self.__class__._default_player_state(),
            left=self.__class__._default_player_state(),
            dora_indicators=["blank"] * 5,
            uradora_indicators=["blank"] * 5,
            round="East 1",
            honba=0,
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
        uradora_indicators = [str(face) for face in gamestate.current_hand.wall.uradora_indicators]
        ndora_revealed = gamestate.current_hand.wall.ndora_revealed
        unrevealed = ["back"] * (5 - ndora_revealed)
        self.state.dora_indicators = dora_indicators[:ndora_revealed] + unrevealed
        self.state.uradora_indicators = uradora_indicators[:ndora_revealed] + unrevealed
        round_wind_str = str(gamestate.current_hand.round_wind).capitalize()
        self.state.round = f"{round_wind_str} {len(gamestate.hands) % 4}"
        self.state.honba = gamestate.current_hand.honba
        self.state.tiles_remaining = gamestate.current_hand.wall.remaining
        self.need_update = True

    def set_commands(self, commands):  # pylint: disable=W0613
        self.need_update = True  # TODO

    def get_command_batch(self):
        self.need_update = True  # TODO

    def on_update(self, delta_time):
        if self.need_update:
            self.drawables.scene.get_sprite_list("tiles").clear()
            self.drawables.gui.clear()
            self._update_scene()
            self._update_gui()
            self.need_update = False

    def on_draw(self):
        self.clear()
        self.drawables.scene.draw()
        self.gui_camera.use()
        self.drawables.gui.draw()
        self.drawables.buttons.draw()

    def _setup(self):
        self.drawables.scene = arcade.Scene()
        self.drawables.scene.add_sprite_list("tiles")
        self.drawables.gui = DrawableList()
        self.drawables.buttons = DrawableList()
        self.gui_camera = arcade.Camera(self.width, self.height)

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

    def _make_button(self, *args, callback=None, **kwargs):
        button = Button(*args, **({"style": config.BUTTON_STYLE} | kwargs))
        button.disable()
        if callback:
            button.event("on_click")(callback)
        return button

    def _add_button(self, *args, callback=None, **kwargs):
        button = self._make_button(*args, callback=callback, **kwargs)
        manager = arcade.gui.UIManager()
        manager.enable()
        manager.add(button)
        self.drawables.buttons.append(manager)

    def _add_tile_button(self, anchor, size, rotation=0, strides=(0, 0), ntiles_offset=0, **kwargs):
        button_offset_x, button_offset_y = {
            0: (0, -self.consts.tile_height),
            90: (0, 0),
            180: (-self.consts.tile_width, 0),
            270: (-self.consts.tile_height, -self.consts.tile_width),
        }[rotation]
        x = anchor[0] + button_offset_x + ntiles_offset * strides[0]
        y = anchor[1] + button_offset_y + ntiles_offset * strides[1]
        width = size[0] if rotation in [0, 180] else size[1]
        height = size[0] if rotation in [90, 270] else size[1]
        self._add_button(x=x, y=y, width=width, height=height, text_rotation=rotation,
                         callback=self._generic_button_callback, **kwargs)

    def _add_tile_row(self, tiles, anchor_x=0, anchor_y=0, rotation=0, buttons=False, **kwargs):
        tile_half_width = self.consts.tile_width // 2
        tile_half_height = self.consts.tile_height // 2
        offset_x, offset_y = {
            0: (tile_half_width, -tile_half_height),
            90: (tile_half_height, tile_half_width),
            180: (-tile_half_width, tile_half_height),
            270: (-tile_half_height, -tile_half_width),
        }[rotation]
        button_offset_x, button_offset_y = {
            0: (0, -(tile_half_height + 5)),
            90: (self.consts.tile_height + 5, 0),
            180: (0, self.consts.tile_height + 5),
            270: (-(tile_half_height + 5), 0),
        }[rotation]
        stride = self.consts.tile_width + 2
        stride_x, stride_y = {0: (stride, 0), 90: (
            0, stride), 180: (-stride, 0), 270: (0, -stride)}[rotation]
        for i, tile in enumerate(tiles):
            self._add_tile(tile, center_x=anchor_x + offset_x + i * stride_x,
                           center_y=anchor_y + offset_y + i * stride_y, rotation=rotation, **kwargs)
            button_size = (self.consts.tile_width, int(0.7 * self.consts.tile_width))
            if buttons:
                self._add_tile_button((anchor_x + button_offset_x, anchor_y + button_offset_y),
                                      button_size, rotation=rotation, strides=(stride_x, stride_y),
                                      ntiles_offset=i, text="cut")

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
        self._add_tile_row(tiles[:13], anchor_x=anchor_x, anchor_y=anchor_y,
                           rotation=rotation, buttons=True)
        if draw:
            self._add_tile_row([draw], anchor_x=anchor_x + draw_offset_x,
                               anchor_y=anchor_y + draw_offset_y, rotation=rotation,
                               buttons=True)

    def _add_dora_indicators(self, tiles):
        self._add_tile_row(tiles[:5], anchor_x=85, anchor_y=2 * self.consts.tile_height + 15 + 3)

    def _add_uradora_indicators(self, tiles):
        self._add_tile_row(tiles[:5], anchor_x=85, anchor_y=self.consts.tile_height + 15)

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
        self._add_uradora_indicators(self.state.uradora_indicators)

    def _make_gui_text(self):
        texts = DrawableList()
        texts.append(arcade.Text(self.state.bottom.wind, self.consts.center_x - 90,
                                 self.consts.center_y - 90, color=arcade.csscolor.WHITE,
                                 rotation=0))
        texts.append(arcade.Text(self.state.right.wind, self.consts.center_x + 90,
                                 self.consts.center_y - 90, color=arcade.csscolor.WHITE,
                                 rotation=90))
        texts.append(arcade.Text(self.state.top.wind, self.consts.center_x + 90,
                                 self.consts.center_y + 90, color=arcade.csscolor.WHITE,
                                 rotation=180))
        texts.append(arcade.Text(self.state.left.wind, self.consts.center_x - 90,
                                 self.consts.center_y + 90, color=arcade.csscolor.WHITE,
                                 rotation=-90))
        texts.append(arcade.Text(str(self.state.bottom.points), self.consts.center_x,
                                 self.consts.center_y - 60, color=arcade.csscolor.WHITE,
                                 rotation=0, font_size=18, anchor_x="center", anchor_y="center"))
        texts.append(arcade.Text(str(self.state.right.points), self.consts.center_x + 60,
                                 self.consts.center_y, color=arcade.csscolor.WHITE,
                                 rotation=90, font_size=18, anchor_x="center", anchor_y="center"))
        texts.append(arcade.Text(str(self.state.top.points), self.consts.center_x,
                                 self.consts.center_y + 60, color=arcade.csscolor.WHITE,
                                 rotation=180, font_size=18, anchor_x="center", anchor_y="center"))
        texts.append(arcade.Text(str(self.state.left.points), self.consts.center_x - 60,
                                 self.consts.center_y, color=arcade.csscolor.WHITE,
                                 rotation=-90, font_size=18, anchor_x="center", anchor_y="center"))
        texts.append(arcade.Text(self.state.round, self.consts.center_x, self.consts.center_y + 15,
                                 color=arcade.csscolor.WHITE, font_size=20, anchor_x="center",
                                 anchor_y="center"))
        texts.append(arcade.Text(f"x{self.state.tiles_remaining}", self.consts.center_x,
                                 self.consts.center_y - 15, color=arcade.csscolor.WHITE,
                                 font_size=15, anchor_x="center", anchor_y="center"))
        texts.append(arcade.Text(f"honba {self.state.honba}", self.consts.center_x,
                                 self.consts.center_y - 36, color=arcade.csscolor.WHITE,
                                 font_size=11, anchor_x="center", anchor_y="center"))
        texts.append(arcade.Text("ura", 275, 50, color=arcade.csscolor.WHITE, rotation=-90))
        texts.append(arcade.Text("dora", 260, 55, color=arcade.csscolor.WHITE, rotation=-90))
        texts.append(arcade.Text("dora", 260, 100, color=arcade.csscolor.WHITE, rotation=-90))
        return texts

    @staticmethod
    def _generic_button_callback(event):
        print(event)

    def _make_player_action_buttons(self, player):
        rel_width = int(1.4 * self.consts.tile_width)
        rel_height = int(0.7 * self.consts.tile_width)
        rotation, align_x, align_y, width, height, vertical, reverse = {
            "bottom": (0, 0, -305, rel_width, rel_height, False, False),
            "right": (90, 305, 0, rel_height, rel_width, True, True),
            "top": (180, 0, 305, rel_width, rel_height, False, True),
            "left": (270, -305, 0, rel_height, rel_width, True, False),
        }[player]
        names = ["draw", "chii", "pon", "kan", "ron", "tsumo", "riichi", "9t9h"]
        if reverse:
            names.reverse()
        box = arcade.gui.UIBoxLayout(vertical=vertical)
        for name in names:
            box.add(self._make_button(
                text=name,
                text_rotation=rotation,
                width=width,
                height=height,
                callback=self._generic_button_callback,
            ).with_space_around(3, 3, 3, 3))
        manager = arcade.gui.UIManager()
        manager.enable()
        manager.add(arcade.gui.UIAnchorWidget(child=box, align_x=align_x, align_y=align_y))
        return manager

    def _make_system_buttons(self):
        names = ["end hand", "end game"]
        box = arcade.gui.UIBoxLayout(vertical=False)
        for name in names:
            box.add(self._make_button(
                text=name,
                width=80,
                height=35,
                callback=self._generic_button_callback,
            ).with_space_around(4, 4, 4, 4))
        manager = arcade.gui.UIManager()
        manager.enable()
        manager.add(arcade.gui.UIAnchorWidget(child=box, anchor_x="left", anchor_y="bottom",
                                              align_x=82, align_y=110))
        return [manager]

    def _make_gui_buttons(self):
        managers = DrawableList()
        players = ["bottom", "right", "left", "top"]
        managers.extend(self._make_player_action_buttons(player) for player in players)
        managers.extend(self._make_system_buttons())
        return managers

    def _update_gui(self):
        gui = DrawableList()
        gui.extend(self._make_gui_text())
        gui.append(RectDrawable(self.consts.center_x - 100, self.consts.center_x + 100,
                                self.consts.center_y + 100, self.consts.center_y - 100,
                                arcade.csscolor.WHITE, border_width=3))
        gui.extend(self._make_gui_buttons())
        self.drawables.gui.extend(gui)


def _run_sync(condition):
    global _visual_context  # pylint: disable=C0103,W0603
    _visual_context = VisualContext()
    if condition:
        with condition:
            condition.notify()
    _visual_context.run()

def run():
    condition = Condition()
    if not _visual_context:
        Thread(target=_run_sync, args=(condition,)).start()
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
