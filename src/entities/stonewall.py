from pytcod import *

from src.entities import Entity


class StoneWall(Entity):
    name = 'stonewall'
    type = 'wall'
    icon = "#"
    fg = Color(90, 104, 110)
    bg = Color(73,58,67)
    block = True

exported_class = StoneWall
