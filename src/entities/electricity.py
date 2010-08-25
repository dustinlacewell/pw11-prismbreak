import random

from pytcod import *
from src.entities import Entity


class Electricity(Entity):
    name = 'electricity'
    icon = "*"
    colors = [
        Color(45, 37, 202),
        Color(80, 71, 255),
        WHITE,
        YELLOW,
        BLUE,
    ]
    fg = BLUE
    bg = Color(31, 33, 37)
    block = False

    def update(self, game):
        level = game.level
        player = game.player

        self.fg = BLUE.lerped(YELLOW, random.random())

    def touched(self, game, ent):
        if ent.name == "player":
            print "PLAYER KILLED"

exported_class = Electricity
