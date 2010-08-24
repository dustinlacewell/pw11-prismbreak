import random

from pytcod import *
from src.entities import Entity


class RobotGuard(Entity):
    name = 'robotguard'
    icon = "R"
    fg = Color(0, 0, 255)
    bg = Color(31, 33, 37)
    block = True
    path = None

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
        map = game.map
        map.compute_fov(self.x, self.y, radius=10, walls=False)
        playercell = map.cell(player.x, player.y)
        if playercell.lit:
            print "PLAYER SEEN"
            if not self.path or self.path.destination != (player.x, player.y):
                path = map.get_path()
                print "PATH MADE"
                if path.compute(self.x, self.y, player.x, player.y):
                    self.path = path
                    print "PATH COMPUTED"
        if self.path:
            dx, dy = self.path.walk()
            actions = []
            if dx > self.x:
                actions.append(self.move_right)
            elif dx < self.x:
                actions.append(self.move_left)
            if dy > self.y:
                actions.append(self.move_down)
            elif dy < self.y:
                actions.append(self.move_up)
            for action in actions:
                action(game)
        

exported_class = RobotGuard
