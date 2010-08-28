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
                if blocker.type == 'guard':
                    game.remove(self)
                    game.remove(blocker)
                    game.add(get('key')(dx, dy))
        super(KeyGuard, self).do_move(game, dx, dy)

    def touched(self, game, ent):
        if ent.type == 'guard':
            game.remove(ent)
            game.remove(self)
            game.add(get('key')(self.x, self.y))


exported_class = KeyGuard
