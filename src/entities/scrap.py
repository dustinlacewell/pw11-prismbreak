from pytcod import *

from src.entities import Entity


class Scrap(Entity):
    name = 'scrap'
    icon =  '%'
    fg = BLUE
    block = False

    def touched(self, game, ent):
        if ent.name == 'player':
            ent.scrap += 1
            game.remove(self)

exported_class = Scrap
