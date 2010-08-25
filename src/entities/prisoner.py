

import random

from pytcod import *
from src.entities import Entity


class Prisoner(Entity):
    name = 'prisoner'
    icon = "P"
    fg = Color(208, 183, 82)
    bg = Color(31, 33, 37)
    block = True

    def update(self, game):
        level = game.level
        player = game.player
        actions = [
            self.move_left,
            self.move_right,
            self.move_up,
            self.move_down,
        ]

        action = random.choice(actions)
        action(game)
        

exported_class = Prisoner
