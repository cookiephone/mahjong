import arcade


class RectDrawable:

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def draw(self):
        arcade.draw_lrtb_rectangle_outline(*self.args, **self.kwargs)
