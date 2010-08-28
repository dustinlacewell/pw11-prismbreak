from pytcod import *

from src.entities import Entity


class Staff(Entity):
    name = 'staff'
    icon =  'J'
    fg = ORANGE

    def touched(self, game, ent):
        if ent.name == 'player':
            game.player.staff = True
            game.remove(self)
            game.show_staff()

exported_class = Staff
