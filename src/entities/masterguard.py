import random

from pytcod import *
from src.entities.robotguard import RobotGuard
from src.entities import get


class MasterGuard(RobotGuard):
    name = 'masterguard'
    type = 'guard'
    icon = "M"
    fg = GREEN
    hp = 5

    def do_move(self, game, dx, dy):
        if self.coord_in_bounds(game, dx, dy):
            blocker = self.thing_at_dest(game, dx, dy)
            if blocker:
                if blocker.name in [game.player.name, 'msgtrigger']:
                    self.x = dx
                    self.y = dy
                    blocker.touched(game, self)
                elif blocker.type == 'guard':
                    game.remove(blocker)
                    game.add(get('scrap')(dx, dy))
                    self.checkfinish()
                elif not blocker.block:
                    self.x = dx
                    self.y = dy
            else:
                self.x = dx
                self.y = dy

    def checkfinish(self, game):
        self.hp -= 1
        if self.hp == 0:
            for ent in game.level.entities:
                if ent.type == guard:
                    game.remove(ent)
                    game.add(get('scrap')(ent.x, ent.y))
                elif ent.name == 'electricity':
                    game.remove(ent)

    def touched(self, game, ent):
        if ent.type == 'guard':
            game.remove(ent)
            game.add(get('scrap')(ent.x, ent.y))
            self.checkfinish()
            


exported_class = MasterGuard
