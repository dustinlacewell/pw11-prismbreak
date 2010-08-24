

class Level(object):

    def __init__(self, app):
        self.w = app.view.width
        self.h = app.view.height

        self.tiles = []
        self.entities = []
	self.links = {}

    def tile_at(self, x, y):
        for t in self.tiles:
            if t.x == x and t.y == y:
                return t

    def ent_at(self, x, y):
        for e in self.entities:
            if e.x == x and e.y == y:
                return e

    def draw(self):
        pass

