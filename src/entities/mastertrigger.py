import random

from pytcod import *
from src.entities import Entity
from src.entities.masterguard import MasterGuard
from src.entities.masterdoor import MasterDoor


class MasterTrigger(Entity):
    name = 'mastertrigger'
    type = 'invis'
    icon = "m"
    fg = BLUE
    bg = YELLOW
    transparent = True
    uuid = "MASTERTRIGGER"
    title = "Suddenly!"
    message = "Major General Screwloose, the Master Guard has appeared at the door."

    def touched(self, game, ent):
        if ent.name == "player":
            if self.uuid not in game.seenmsgs:
                game.set_frame(50, 5, self.message, self.title, wrapped=True)
                game.seenmsgs.add(self.uuid)
                g = MasterGuard( 40, 40)
                print "GUARD CREATED"
                game.add(g)
                remove = []
                uuid = 'MASTERDOOR1'
                for entity in game.level.entities:
                    if entity.name == 'door':
                        remove.append(entity)
                for door in remove:
                    game.level.entities.remove(door)
                    game.add(MasterDoor(door.x, door.y, uuid))
exported_class = MasterTrigger
