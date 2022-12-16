class DrawableList(list):

    def draw(self):
        for elem in self:
            elem.draw()
