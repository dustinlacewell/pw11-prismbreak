from pytcod import *

from src.entities import Entity


class MasterKey(Entity):
    name = 'masterkey'
    icon =  '{'
    fg = GREEN

    def touched(self, game, ent):
        if ent.name == 'player':
            game.player.masterkey = True
            game.remove(self)
            game.set_frame(30, 4, "Jeeze this key is almost as big as I am.", "Wizard says:")

exported_class = MasterKey
