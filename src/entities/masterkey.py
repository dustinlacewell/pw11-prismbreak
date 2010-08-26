from pytcod import *

from src.entities import Entity


class MasterKey(Entity):
    name = 'key'
    icon =  '{'
    fg = GREEN

    def touched(self, game, ent):
        if ent.name == 'player':
            player.masterkey = True
            game.remove(self)

exported_class = MasterKey
