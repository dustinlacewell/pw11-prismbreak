import random

from pytcod import *
from src.entities import Entity


class RobotGuard(Entity):
    name = 'robotguard'
    icon = "R"
    fg = Color(0, 0, 255)
    bg = Color(31, 33, 37)
    block = True

    def do_move(self, game, dx, dy):
        if self.coord_in_bounds(game, dx, dy):
            blocker = self.thing_at_dest(game, dx, dy)
            if blocker:
                if blocker.name == self.name:
                    self.x = dx
                    self.y = dy
                    blocker.touched(game, self)
            else:
                self.x = dx
                self.y = dy

    def touched(self, game, ent):
        if ent.name == 'robotguard':
            game.remove(ent)
            game.remove(self)

    def update(self, game):
        level = game.level
        player = game.player
        actions = []
        if player.x > self.x:
            actions.append(self.move_right)
        elif player.x < self.x:
            actions.append(self.move_left)
        if player.y > self.y:
            actions.append(self.move_down)
        elif player.y < self.y:
            actions.append(self.move_up)
        action = random.choice(actions)
        action(game)
        

exported_class = RobotGuard
