import random
from copy import copy

from pytcod import *
from src.entities import Entity


class Player(Entity):
    name = 'player'
    icon = "W"
    fg = Color(100, 63, 161)
    bg = Color(31, 33, 37)
    block = True
    scrap = 0

    def touched(self, game, ent):
        if ent.name == 'robotguard':
            game.player_death(ent)

exported_class = Player
