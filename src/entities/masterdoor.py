import random

from pytcod import *
from src.entities import Entity


class MasterDoor(Entity):
    name = 'masterdoor'
    type = 'door'
    icon = "+"
    fg = GREEN
    bg = YELLOW
    block = True
    transparent = False
    uuid = 'masterdoor'

    def update(self, game):
        p = game.player
        xdif = abs(p.x - self.x)
        ydif = abs(p.y - self.y)
        if xdif == 1 and ydif == 0 or xdif == 0 and ydif == 1 or xdif == 1 and ydif == 1:
            if p.masterkey:
                game.opendoor(self.uuid)

exported_class = MasterDoor
