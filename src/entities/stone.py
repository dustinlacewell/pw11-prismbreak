from pytcod import *

from src.entities import Entity


class Stone(Entity):
    name = 'stone'
    icon = "#"
    fg = Color(90, 104, 110)
    bg = Color(153, 182, 196)
    block = True

exported_class = Stone
