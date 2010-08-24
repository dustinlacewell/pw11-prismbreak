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

    def update(self, app, level, player):
        pass
