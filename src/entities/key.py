from pytcod import *

from src.entities import Entity


class Key(Entity):
    name = 'key'
    icon =  '{'
    fg = YELLOW
    block = False

    def touched(self, game, ent):
        if ent.name == 'player':
            game.keys += 1
            game.remove(self)

exported_class = Key
