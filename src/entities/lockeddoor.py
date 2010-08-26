import random

from pytcod import *
from src.entities import Entity


class LockedDoor(Entity):
    name = 'lockeddoor'
    icon = "+"
    fg = YELLOW
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
            if game.keys and game.opendoor(self.uuid, locked=True):
                game.keys -= 1
                game.set_frame(20, 3, "Door opened.", "", wrapped=True)

exported_class = LockedDoor
