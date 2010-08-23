from pytcod import *

from src.entities import Entity

class GroundWood(Entity):
    name = 'ground-wood'
    icon = "%"
    fg = Color(167, 104, 47)
    bg = Color(98, 66, 38)
    block = True

exported_class = GroundWood
