import random

from pytcod import *
from src.entities import Entity


class MsgTrigger(Entity):
    name = 'msgtrigger'
    type = 'invis'
    icon = "m"
    fg = BLUE
    bg = YELLOW
    block = False
    transparent = True
    uid = None

    def __init__(self, x, y, uuid, message, title):
        self.uuid = uuid
        self.title = title
        self.message = message
        super(MsgTrigger, self).__init__(x, y)

    def touched(self, game, ent):
        if ent.name == "player":
            if self.uuid not in game.seenmsgs:
                game.set_frame(34, len(self.message) / 34 + 5, self.message, self.title, wrapped=True)
                game.seenmsgs.add(self.uuid)

exported_class = MsgTrigger
