import random

from pytcod import *
from src.entities import Entity
from src.entities.masterguard import MasterGuard
from src.entities.masterdoor import MasterDoor
from src.scenes import get

class WinTrigger(Entity):
    name = 'wintrigger'
    type = 'invis'
    icon = "m"
    fg = BLUE
    bg = YELLOW
    transparent = True
    uuid = "WINTRIGGER"

    def touched(self, game, ent):
        if ent.name == "player":
            if self.uuid not in game.seenmsgs:
                game.app.scene = get('credits')()
exported_class = WinTrigger
