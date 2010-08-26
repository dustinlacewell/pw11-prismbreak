from pytcod import *

from src.entities import Entity


class Exit(Entity):
    name = 'exit'
    block = False

    def __init__(self, x, y, linkname):
        self.linkname = linkname
        super(Exit, self).__init__(x, y)

    def touched(self, game, ent):
        if ent.name == 'player':
            p = game.player
            game.lastlevel = game.levelname
            sx, sy = game.load(self.linkname)
            p.x = sx
            p.y = sy

exported_class = Exit
