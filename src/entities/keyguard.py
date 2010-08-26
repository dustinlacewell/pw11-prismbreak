import random

from pytcod import *
from src.entities.robotguard import RobotGuard
from src.entities import get


class KeyGuard(RobotGuard):
    name = 'keyguard'
    type = 'guard'
    icon = "K"
    fg = YELLOW

    def do_move(self, game, dx, dy):
        if self.coord_in_bounds(game, dx, dy):
            blocker = self.thing_at_dest(game, dx, dy)
            if blocker:
                if blocker.name in [game.player.name, 'msgtrigger']:
                    self.x = dx
                    self.y = dy
                    blocker.touched(game, self)
                elif blocker.type == 'guard':
                    game.remove(self)
                    game.remove(blocker)
                    game.add(get('key')(dx, dy))
            else:
                self.x = dx
                self.y = dy

    def touched(self, game, ent):
        print "KEYGUARD TOUCHED"
        if ent.type == 'guard':
            game.remove(ent)
            game.remove(self)
            game.add(get('key')(self.x, self.y))


exported_class = KeyGuard
