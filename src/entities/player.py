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
        print "PLAYER TOUCHED"
        if ent.name == 'robotguard':
            p = game._player
            game.load(game.levelname)
            game.player = p
            game._player = copy(game.player)

exported_class = Player
