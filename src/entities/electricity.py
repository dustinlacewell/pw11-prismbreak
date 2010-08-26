import random

from pytcod import *
from src.entities import Entity


class Electricity(Entity):
    name = 'electricity'
    type = 'electricity'
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

    def update(self, game):
        level = game.level
        player = game.player
        self.fg = BLUE.lerped(YELLOW, random.random())

    def touched(self, game, ent):
        if ent.name == "player":
            game.player_death(self)

exported_class = Electricity
