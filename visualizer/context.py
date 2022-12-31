from types import SimpleNamespace
from threading import Thread, Condition
import math
import arcade
import arcade.gui
from visualizer import config
from visualizer.button import Button
from visualizer.drawables import DrawableList, RectDrawable, RiichiStickDrawable
from mahjong.utils import parsing
from mahjong.seats import Seat
from mahjong.melds import Mentsu


# god is dead and this file killed him
_visual_context = None  # pylint: disable=C0103


class VisualContext(arcade.Window):

    def __init__(self):
        super().__init__(width=config.SCREEN_WIDTH, height=config.SCREEN_HEIGHT,
                         title=config.SCREEN_TITLE, update_rate=config.UPDATE_RATE)
        arcade.set_background_color(arcade.color.DIM_GRAY)
        mock = arcade.Sprite(
            filename=config.TILE_IMAGES["front"], scale=config.TILE_SCALING)
        self.consts = SimpleNamespace(
            center_x=self.width // 2,
            center_y=self.height // 2,
            tile_width=mock.width,
            tile_height=mock.height,
            tile_half_width = mock.width // 2,
            tile_half_height = mock.height // 2)
        self.drawables = SimpleNamespace(tiles=None, gui=None, buttons=None, sticks=None)
        self.gui_camera = None
        self.state = SimpleNamespace(
            bottom=self._default_player_state("bottom"),
            right=self._default_player_state("right"),
            top=self._default_player_state("top"),
            left=self._default_player_state("left"),
            dora_indicators=["blank"] * 5,
            uradora_indicators=["blank"] * 5,
            round="East 1",
            honba=0,
            tiles_remaining=35)
        self.state.players = [self.state.bottom, self.state.right, self.state.top, self.state.left]
        self.need_update = False
        self._setup()

    def set_gamestate(self, gamestate):
        for player, pstate in zip(gamestate.current_hand.players, self.state.players):
            pstate.points = player.points
            pstate.wind = str(player.seat).capitalize()
            pstate.discards = [str(tile) for tile in player.discards]
            sorted_hand = parsing.tileset_from_string(parsing.tileset_to_string(player.hand))
            pstate.hand = [str(tile) for tile in sorted_hand]
            pstate.draw = str(player.drawn_tile()) if player.drawn_tile() else None
            pstate.melds = [self._meld_as_state(meld, player) for meld in player.called_melds]
            # TODO: get riichi status/riichi-discard of player
            # TODO: (consider riichi discard called and rediscarded!)
            pstate.riichi = math.nan
        dora_indicators = [str(face) for face in gamestate.current_hand.wall.dora_indicators]
        uradora_indicators = [str(face) for face in gamestate.current_hand.wall.uradora_indicators]
        ndora_revealed = gamestate.current_hand.wall.ndora_revealed
        unrevealed = ["back"] * (5 - ndora_revealed)
        self.state.dora_indicators = dora_indicators[:ndora_revealed] + unrevealed
        self.state.uradora_indicators = uradora_indicators[:ndora_revealed] + unrevealed
        round_wind_str = str(gamestate.current_hand.round_wind).capitalize()
        self.state.round = f"{round_wind_str} {gamestate.round}"
        self.state.honba = gamestate.current_hand.honba
        self.state.tiles_remaining = gamestate.current_hand.wall.remaining
        self.need_update = True

    def set_commands(self, commands):  # pylint: disable=W0613
        self.need_update = True  # TODO

    def get_command_batch(self):
        self.need_update = True  # TODO

    def on_update(self, delta_time):
        if self.need_update:
            self.drawables.tiles.clear()
            self.drawables.gui.clear()
            self.drawables.sticks.clear()
            self._update_scene()
            self._update_gui()
            self.need_update = False

    def on_draw(self):
        self.clear()
        self.drawables.tiles.draw()
        self.gui_camera.use()
        self.drawables.gui.draw()
        self.drawables.buttons.draw()
        self.drawables.sticks.draw()

    def _setup(self):
        self.drawables.tiles = arcade.SpriteList()
        self.drawables.gui = DrawableList()
        self.drawables.buttons = DrawableList()
        self.drawables.sticks = DrawableList()
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
        self.drawables.tiles.append(background)
        self.drawables.tiles.append(face)

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
        width = size[0] if rotation in {0, 180} else size[1]
        height = size[0] if rotation in {90, 270} else size[1]
        self._add_button(x=x, y=y, width=width, height=height, text_rotation=rotation,
                         callback=self._generic_button_callback, **kwargs)

    def _add_tile_row(self, tiles, anchor=(0, 0), rotation=0, buttons=False, riichi=None, **kwargs):
        stride = self.consts.tile_width + 2
        offset_x, offset_y, button_offset_x, button_offset_y, stride_x, stride_y, riichi_sign = {
            0: (self.consts.tile_half_width, -self.consts.tile_half_height,
                0, -(self.consts.tile_half_height + 5), stride, 0, 1),
            90: (self.consts.tile_half_height, self.consts.tile_half_width,
                self.consts.tile_height + 5, 0, 0, stride, 1),
            180: (-self.consts.tile_half_width, self.consts.tile_half_height,
                0, self.consts.tile_height + 5, -stride, 0, -1),
            270: (-self.consts.tile_half_height, -self.consts.tile_half_width,
                -(self.consts.tile_half_height + 5), 0, 0, -stride, -1),
        }[rotation]
        riichi_offset = riichi_sign * (self.consts.tile_height - self.consts.tile_width) // 2
        riichi_offset_x = riichi_offset if stride_x != 0 else 0
        riichi_offset_y = riichi_offset if stride_y != 0 else 0
        running_riichi_offset_x, running_riichi_offset_y = 0, 0
        for i, tile in enumerate(tiles):
            if i == riichi:
                running_riichi_offset_x += riichi_offset_x
                running_riichi_offset_y += riichi_offset_y
            self._add_tile(
                tile,
                center_x=anchor[0] + offset_x + running_riichi_offset_x + i * stride_x,
                center_y=anchor[1] + offset_y + running_riichi_offset_y + i * stride_y,
                rotation=rotation - (90 if i == riichi else 0),
                **kwargs)
            if i == riichi:
                running_riichi_offset_x += riichi_offset_x
                running_riichi_offset_y += riichi_offset_y
            button_size = (self.consts.tile_width, int(0.7 * self.consts.tile_width))
            if buttons:
                self._add_tile_button((anchor[0] + button_offset_x, anchor[1] + button_offset_y),
                                      button_size, rotation=rotation, strides=(stride_x, stride_y),
                                      ntiles_offset=i, text="cut")

    def _add_discard_pile(self, player):
        row_offset = self.consts.tile_height + 2
        offset_x, offset_y, row_offset_x, row_offset_y, rotation = {
            "bottom": (103, 110, 0, row_offset, 0),
            "right": (-110, 103, -row_offset, 0, 90),
            "top": (-103, -110, 0, -row_offset, 180),
            "left": (110, -103, row_offset, 0, 270),
        }[player.position]
        self._add_tile_row(
            player.discards[:6],
            anchor=(
                self.consts.center_x - offset_x,
                self.consts.center_y - offset_y),
            rotation=rotation,
            riichi=player.riichi)
        self._add_tile_row(
            player.discards[6:12],
            anchor=(
                self.consts.center_x - offset_x - row_offset_x,
                self.consts.center_y - offset_y - row_offset_y),
            rotation=rotation,
            riichi=player.riichi - 6)
        self._add_tile_row(
            player.discards[12:],
            anchor=(
                self.consts.center_x - offset_x - 2 * row_offset_x,
                self.consts.center_y - offset_y - 2 * row_offset_y),
            rotation=rotation,
            riichi=player.riichi - 12)

    def _add_hand(self, player):
        draw_offset = len(player.hand) * (self.consts.tile_width + 2) + 10
        hand_offset = 4 * (self.consts.tile_width + 2)
        offset_x, offset_y, draw_offset_x, draw_offset_y, rotation = {
            "bottom": (103 + hand_offset, 330, draw_offset, 0, 0),
            "right": (-330, 103 + hand_offset, 0, draw_offset, 90),
            "top": (-103 - hand_offset, -330, -draw_offset, 0, 180),
            "left": (330, -103 - hand_offset, 0, -draw_offset, 270),
        }[player.position]
        anchor_x, anchor_y = self.consts.center_x -  offset_x, self.consts.center_y - offset_y
        self._add_tile_row(
            player.hand[:13],
            anchor=(anchor_x, anchor_y),
            rotation=rotation,
            buttons=True)
        if player.draw:
            self._add_tile_row(
                [player.draw],
                anchor=(anchor_x + draw_offset_x, anchor_y + draw_offset_y),
                rotation=rotation, buttons=True)

    def _add_dora_indicators(self, tiles):
        self._add_tile_row(tiles[:5], anchor=(85, 2 * self.consts.tile_height + 15 + 3))

    def _add_uradora_indicators(self, tiles):
        self._add_tile_row(tiles[:5], anchor=(85, self.consts.tile_height + 15))

    def _ensure_meld_tile_order(self, m):
        called_idx = {
            None: math.nan,
            Seat.SHIMOCHA: 0,
            Seat.TOIMEN: -2,
            Seat.KAMICHA: 2
        }[m.called_seat] % len(m.tiles)
        if Mentsu.CHII in m.variant and m.called_seat:
            tile_idx = m.tiles.index(m.called_tile)
            m.tiles[tile_idx], m.tiles[called_idx] = m.tiles[called_idx], m.tiles[tile_idx]
        added_idx = -1 % len(m.tiles) if Mentsu.ADDED in m.variant else math.nan
        hidden_idxs = {0, 3} if Mentsu.ANKAN in m.variant else {}
        return m.tiles, called_idx, added_idx, hidden_idxs

    def _add_meld(self, m, anchor_x=0, anchor_y=0, rotation=0, offset=0):
        tiles, called_idx, added_idx, hidden_idxs = self._ensure_meld_tile_order(m)
        offset_x, offset_y, hor_x, hor_y = {
            0: (offset, 0, -1, 0),
            90: (0, offset, 0, -1),
            180: (-offset, 0, 1, 0),
            270: (0, -offset, 0, 1),
        }[rotation]
        tile_delta = self.consts.tile_half_width - self.consts.tile_half_height - 1
        fix_sign = -1 if rotation in {0, 180} else 1
        new_offset = 0
        for i, tile in enumerate(reversed(tiles)):
            pre_offset = self.consts.tile_half_width
            post_offset = self.consts.tile_half_width + 2
            true_rotation = rotation
            true_fix_x = 0
            true_fix_y = 0
            if i in {called_idx, added_idx}:
                pre_offset = self.consts.tile_half_height + 1
                post_offset = self.consts.tile_half_height + 3
                true_rotation = rotation - 90
                true_fix_x = hor_y * tile_delta * fix_sign
                true_fix_y = hor_x * tile_delta * fix_sign
            if i == added_idx:
                pre_offset = -(self.consts.tile_half_height + 3)
                true_fix_x += hor_y * fix_sign * (self.consts.tile_width + 2)
                true_fix_y += hor_x * fix_sign * (self.consts.tile_width + 2)
            if i in hidden_idxs:
                tile = "back"
            new_offset += pre_offset
            self._add_tile(
                tile,
                rotation=true_rotation,
                center_x=anchor_x + offset_x + true_fix_x + hor_x * new_offset,
                center_y=anchor_y + offset_y + true_fix_y + hor_y * new_offset)
            new_offset += post_offset
        return offset - new_offset

    def _add_melds(self, player):
        lift = self.consts.tile_half_height + 10
        anchor_x, anchor_y, rotation = {
            "bottom": (self.width - 40, lift, 0),
            "right": (self.width - lift, self.height - 40, 90),
            "top": (40, self.height - lift, 180),
            "left": (lift, 40, 270),
        }[player.position]
        offset = 0
        for m in player.melds:
            offset += self._add_meld(
                m,
                anchor_x=anchor_x,
                anchor_y=anchor_y,
                rotation=rotation,
                offset=offset)

    def _add_riichi_stick(self, player):
        if not math.isnan(player.riichi):
            offset_x, offset_y, rotate = {
                "bottom": (0, -90, False),
                "right": (90, 0, True),
                "top": (0, 90, False),
                "left": (-90, 0, True),
            }[player.position]
            self.drawables.sticks.append(RiichiStickDrawable(
                center_x=self.consts.center_x + offset_x,
                center_y=self.consts.center_y + offset_y,
                scale=1.1,
                rotate=rotate))

    def _update_scene(self):
        for player in self.state.players:
            self._add_discard_pile(player)
            self._add_hand(player)
            self._add_melds(player)
            self._add_riichi_stick(player)
        self._add_dora_indicators(self.state.dora_indicators)
        self._add_uradora_indicators(self.state.uradora_indicators)

    def _make_gui_text(self):
        texts = DrawableList()
        texts.append(arcade.Text(self.state.bottom.wind, self.consts.center_x - 90,
                                 self.consts.center_y - 90, color=arcade.color.WHITE,
                                 rotation=0))
        texts.append(arcade.Text(self.state.right.wind, self.consts.center_x + 90,
                                 self.consts.center_y - 90, color=arcade.color.WHITE,
                                 rotation=90))
        texts.append(arcade.Text(self.state.top.wind, self.consts.center_x + 90,
                                 self.consts.center_y + 90, color=arcade.color.WHITE,
                                 rotation=180))
        texts.append(arcade.Text(self.state.left.wind, self.consts.center_x - 90,
                                 self.consts.center_y + 90, color=arcade.color.WHITE,
                                 rotation=-90))
        texts.append(arcade.Text(str(self.state.bottom.points), self.consts.center_x,
                                 self.consts.center_y - 60, color=arcade.color.WHITE,
                                 rotation=0, font_size=18, anchor_x="center", anchor_y="center"))
        texts.append(arcade.Text(str(self.state.right.points), self.consts.center_x + 60,
                                 self.consts.center_y, color=arcade.color.WHITE,
                                 rotation=90, font_size=18, anchor_x="center", anchor_y="center"))
        texts.append(arcade.Text(str(self.state.top.points), self.consts.center_x,
                                 self.consts.center_y + 60, color=arcade.color.WHITE,
                                 rotation=180, font_size=18, anchor_x="center", anchor_y="center"))
        texts.append(arcade.Text(str(self.state.left.points), self.consts.center_x - 60,
                                 self.consts.center_y, color=arcade.color.WHITE,
                                 rotation=-90, font_size=18, anchor_x="center", anchor_y="center"))
        texts.append(arcade.Text(self.state.round, self.consts.center_x, self.consts.center_y + 15,
                                 color=arcade.color.WHITE, font_size=20, anchor_x="center",
                                 anchor_y="center"))
        texts.append(arcade.Text(f"x{self.state.tiles_remaining}", self.consts.center_x,
                                 self.consts.center_y - 15, color=arcade.color.WHITE,
                                 font_size=15, anchor_x="center", anchor_y="center"))
        texts.append(arcade.Text(f"honba {self.state.honba}", self.consts.center_x,
                                 self.consts.center_y - 36, color=arcade.color.WHITE,
                                 font_size=11, anchor_x="center", anchor_y="center"))
        texts.append(arcade.Text("ura", 275, 50, color=arcade.color.WHITE, rotation=-90))
        texts.append(arcade.Text("dora", 260, 55, color=arcade.color.WHITE, rotation=-90))
        texts.append(arcade.Text("dora", 260, 100, color=arcade.color.WHITE, rotation=-90))
        return texts

    def _make_player_action_buttons(self, player):
        rel_width = int(1.4 * self.consts.tile_width)
        rel_height = int(0.7 * self.consts.tile_width)
        rotation, align_x, align_y, width, height, vertical, reverse = {
            "bottom": (0, 0, -305, rel_width, rel_height, False, False),
            "right": (90, 305, 0, rel_height, rel_width, True, True),
            "top": (180, 0, 305, rel_width, rel_height, False, True),
            "left": (270, -305, 0, rel_height, rel_width, True, False),
        }[player.position]
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
        submission_button = self._make_button(
            text="submit commands",
            width=168,
            height=35,
            callback=self._generic_button_callback)
        manager.add(arcade.gui.UIAnchorWidget(child=submission_button, anchor_x="left",
                                              anchor_y="bottom", align_x=86, align_y=157))
        manager.add(submission_button)
        return [manager]

    def _make_gui_buttons(self):
        managers = DrawableList()
        managers.extend(self._make_player_action_buttons(player) for player in self.state.players)
        managers.extend(self._make_system_buttons())
        return managers

    def _update_gui(self):
        gui = DrawableList()
        gui.extend(self._make_gui_text())
        gui.append(RectDrawable(self.consts.center_x - 100, self.consts.center_x + 100,
                                self.consts.center_y + 100, self.consts.center_y - 100,
                                arcade.color.WHITE, border_width=3))
        gui.extend(self._make_gui_buttons())
        self.drawables.gui.extend(gui)

    @staticmethod
    def _default_player_state(position):
        return SimpleNamespace(
            position=position,
            points=30000,
            wind="East",
            discards=["blank"] * 15,
            hand=["blank"] * 14,
            melds=[],
            draw="blank",
            riichi=math.nan)

    @staticmethod
    def _meld_as_state(called_meld, owner):
        is_open = called_meld.is_open()
        return SimpleNamespace(
            variant=called_meld.variant,
            tiles=[str(tile) for tile in called_meld.tiles],
            called_tile=str(called_meld.called_tile) if is_open else None,
            called_seat=owner.seat.relative(called_meld.called_player.seat) if is_open else None,
            open=is_open)

    @staticmethod
    def _generic_button_callback(event):
        print(event)


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
