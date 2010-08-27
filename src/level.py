

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
        nonbots = []
        for e in self.entities:
            if e.x == x and e.y == y:
                if e.type != 'guard':
                    nonbots.append(e)
                else:
                    return e
        if nonbots:
            return nonbots[0]

    def draw(self):
        pass

                

