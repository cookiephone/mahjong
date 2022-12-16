import arcade


# improve use of style because its awful in the library implementation
# add enabled/disabled state to button
# also, blending is completely broken in the arcade library, so no semi-transparent buttons
class Button(arcade.gui.UIFlatButton):

    def __init__(self, text_rotation, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.text_rotation = text_rotation
        self.enabled = True

    def enable(self):
        self.enabled = True

    def disable(self):
        self.enabled = False

    # add hovered state style params as documented but missing in the library
    def do_render(self, surface):
        self.prepare_render(surface)
        # render button
        font_size = self._style.get("font_size", 15)
        font_color = self._style.get("font_color", arcade.color.WHITE)
        border_width = self._style.get("border_width", 2)
        border_color = self._style.get("border_color", None)
        bg_color = self._style.get("bg_color", (21, 19, 21))
        # handle states
        if self.pressed and self.enabled:
            bg_color = self._style.get("bg_color_pressed", arcade.color.WHITE)
            border_color = self._style.get("border_color_pressed", arcade.color.WHITE)
            font_color = self._style.get("font_color_pressed", arcade.color.BLACK)
        elif self.hovered and self.enabled:
            bg_color = self._style.get("bg_color_hovered", arcade.color.DARK_GRAY)
            border_color = self._style.get("border_color_hovered", None)
            font_color = self._style.get("font_color_hovered", arcade.color.WHITE)
        elif not self.enabled:
            bg_color = self._style.get("bg_color_disabled", arcade.color.LIGHT_GRAY)
            border_color = self._style.get("border_color_disabled", None)
            font_color = self._style.get("font_color_disabled", arcade.color.WHITE)
        # render background
        if bg_color:
            arcade.draw_xywh_rectangle_filled(0, 0, self.width, self.height, color=bg_color)
        # render border
        if border_color and border_width:
            arcade.draw_xywh_rectangle_outline(
                border_width,
                border_width,
                self.width - 2 * border_width,
                self.height - 2 * border_width,
                color=border_color,
                border_width=border_width)
        # render text
        if self.text:
            start_x = self.width // 2
            start_y = self.height // 2
            text_margin = 2
            arcade.Text(
                text=self.text,
                start_x=start_x,
                start_y=start_y,
                font_size=font_size,
                color=font_color,
                align="center",
                anchor_x="center", anchor_y="center",
                width=self.width - 2 * border_width - 2 * text_margin,
                rotation=self.text_rotation).draw()
