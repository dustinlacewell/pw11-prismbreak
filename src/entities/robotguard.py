import random

from pytcod import *
from src.entities import Entity, get


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
                print "robot blocked by", blocker.name
                if blocker.name in [self.name, game.player.name]:
                    self.x = dx
                    self.y = dy
                    blocker.touched(game, self)
            else:
                self.x = dx
                self.y = dy

    def _get_fg(self):
        return RED if self.path else BLUE
    fg = property(_get_fg)

    def touched(self, game, ent):
        if ent.name == 'robotguard':
            game.remove(ent)
            game.remove(self)
            game.add(get('scrap')(self.x, self.y))

    def update(self, game):
        level = game.level
        player = game.player
        map = game.map
        fov = int(game.app.conf.get('game', 'bot_fov'))
        map.compute_fov(self.x, self.y, radius=fov, walls=False)
        playercell = map.cell(player.x, player.y)
        if playercell.lit:
            if not self.path:
                path = map.get_path()
                if path.compute(self.x, self.y, player.x, player.y):
                    self.path = path
                return
            elif self.path.destination != (player.x, player.y):
                path = map.get_path()
                if path.compute(self.x, self.y, player.x, player.y):
                    self.path = path
        if self.path:
            newpos = self.path.walk()
            if newpos:
                dx, dy = newpos
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
