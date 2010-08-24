from pytcod import *

from src import imports

def get( command_name ):
    """Return the command class for the given command-name."""
    return imports.get('entities', command_name)

class Entity(object):
    name = 'none'
    icon = 'X'
    fg = Color(0, 0, 255)
    bg = Color(255, 0, 0)
    block = False

    
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def coord_in_bounds(self, game, x, y):
        level = game.level
        return 0 <= x < level.w and \
            0 <= y < level.h

    def thing_at_dest(self, game, x, y):
        level = game.level
        ent = level.ent_at(x, y)
        if ent:
            return ent
        tile = level.tile_at(x, y)
        if tile:
            return tile

    def touched(self, game, ent):
        pass

    def update(self, game):
        pass

    def do_move(self, game, dx, dy):
        if self.coord_in_bounds(game, dx, dy):
            blocker = self.thing_at_dest(game, dx, dy)
            if not blocker or (blocker and not blocker.block):
                self.x = dx
                self.y = dy
                if blocker:
                    blocker.touched(game, self)



    def move_left(self, game):
        dx = self.x - 1
        dy = self.y
        self.do_move(game, dx, dy)

    def move_right(self, game):
        dx = self.x + 1
        dy = self.y
        self.do_move(game, dx, dy)

    def move_up(self, game):
        dx = self.x
        dy = self.y - 1
        self.do_move(game, dx, dy)

    def move_down(self, game):
        dx = self.x
        dy = self.y + 1
        self.do_move(game, dx, dy)


