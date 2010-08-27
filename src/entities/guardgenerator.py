from random import randint

from pytcod import *

from src.entities import Entity
from src.entities.robotguard import RobotGuard

class GuardGenerator(Entity):
    name = 'guardgenerator'
    icon = chr(CHAR_RADIO_UNSET)
    fg = LIGHT_BLUE
    block = False
    transparent = True
    delay = 4

    def __init__(self, x, y):
        self._delay = self.delay
        self.guard = None
        super(GuardGenerator, self).__init__(x, y)
        
    def reset_guard(self, game):
        self.guard = RobotGuard(self.x, self.y, randint(100000000, 999999999))
        game.level.entities.append(self.guard)

    def update(self, game):
        if self.guard not in game.level.entities:
            if self._delay == self.delay:
                self.reset_guard(game)
                self._delay = 0
            else:
                self._delay += 1
        if self.guard:
            if self.guard.x == self.x and self.guard.y == self.y:
                self.icon = chr(CHAR_RADIO_SET)
                self.fg = LIGHT_BLUE
            elif self._delay == self.delay:
                self.fg = RED
            else:
                self.icon = chr(CHAR_RADIO_UNSET)
        
exported_class = GuardGenerator
