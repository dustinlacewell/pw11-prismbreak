import random

from pytcod import *
from src.entities import Entity


class MasterDoor(Entity):
    name = 'masterdoor'
    icon = "+"
    fg = GREEN
    bg = YELLOW
    block = True
    transparent = False
    uuid = None

    def __init__(self, x, y, uuid):
        self.uuid = uuid
        super(LockedDoor, self).__init__(x, y)

    def update(self, game):
        p = game.player
        xdif = abs(p.x - self.x)
        ydif = abs(p.y - self.y)
        if xdif == 1 and ydif == 0 or \
        xdif == 0 and ydif == 1 or \
        xdif == 0 and ydif == 0:
            if player.masterkey:
                for entity in game.level.entities:
                    if entity.name == 'masterdoor':
                        game.remove(entity)
                game.masterdoor = True
                game.set_frame(20, 3, "Master door opened!", "", wrapped=True)

exported_class = MasterDoor
