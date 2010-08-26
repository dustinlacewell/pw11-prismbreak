import random

from pytcod import *
from src.entities import Entity, get


class RobotGuard(Entity):
    name = 'robotguard'
    icon = "R"
    type = 'guard'
    fg = Color(0, 0, 255)
    bg = Color(31, 33, 37)
    uuid = None
    block = True
    path = None
    stun = 0
    
    def __init__(self, x, y, uuid):
        self.uuid = uuid
        super(RobotGuard, self).__init__(x, y)

    def do_move(self, game, dx, dy):
        if self.coord_in_bounds(game, dx, dy):
            blocker = self.thing_at_dest(game, dx, dy)
            if blocker:
                print "p", self.x, self.y, game.player.x, game.player.y
                print "robot blocked by", blocker.name
                if blocker.name in [self.name, game.player.name, 'msgtrigger']:
                    self.x = dx
                    self.y = dy
                    blocker.touched(game, self)
            else:
                self.x = dx
                self.y = dy

    def _get_fg(self):
        return RED if self.path else BLUE
    fg = property(_get_fg)

    def pathlength(self):
        if self.path:
            return self.path.size
        return -1

    def touched(self, game, ent):
        if ent.name == 'robotguard':
            game.remove(ent)
            game.remove(self)
            game.add(get('scrap')(self.x, self.y))

    def set_path(self, game):
        p = game.player
        path = game.map.get_path()
        if path.compute(self.x, self.y, p.x, p.y):
            self.path = path

    def update_path(self, game):
        player = game.player
        map = game.map
        fov = int(game.app.conf.get('game', 'bot_fov'))
        map.compute_fov(self.x, self.y, radius=fov, walls=False)
        playercell = map.cell(player.x, player.y)
        if playercell.lit:
            if not self.path:
                self.set_path(game)
                self.stun = 1
            elif self.path.destination != (player.x, player.y):
                self.set_path(game)
    def update(self, game):
        p = game.player
        if (p.x, p.y) == (self.x, self.y):
            print "Player teleported on me"
            self.do_move(game, self.x, self.y)
            return
        if self.path:
            if self.stun:
                self.stun -= 1
            else:
                newpos = self.path.walk()
                if newpos:
                    dx, dy = newpos
                    self.do_move(game, dx, dy)
        

exported_class = RobotGuard
