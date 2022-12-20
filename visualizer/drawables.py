import arcade


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


class RiichiStickDrawable:

    def __init__(self, center_x, center_y, scale=1, rotate=True):
        self.center_x = center_x
        self.center_y = center_y
        self.length = int(65.0 * scale)
        self.girth = int(7.0 * scale)
        self.point_radius = int(3.0 * scale)
        self.tilt_angle = 90 if rotate else 0

    def draw(self):
        arcade.draw_rectangle_filled(
            center_x=self.center_x,
            center_y=self.center_y,
            width=self.length,
            height=self.girth,
            color=(245, 240, 235),
            tilt_angle=self.tilt_angle)
        arcade.draw_circle_filled(
            center_x=self.center_x,
            center_y=self.center_y,
            radius=self.point_radius,
            color=arcade.color.RED,
            tilt_angle=self.tilt_angle)
