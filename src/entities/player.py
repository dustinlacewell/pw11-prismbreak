import random

from pytcod import *
from src.entities import Entity


class Player(Entity):
    name = 'player'
    icon = "W"
    fg = Color(100, 63, 161)
    bg = Color(31, 33, 37)
    block = True

exported_class = Player
