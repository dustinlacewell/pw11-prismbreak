from pytcod import *
from src.entities import Entity


class BloodLight(Entity):
    name = 'bloodlight'
    icon = chr(CHAR_BLOCK1)
    fg = Color(162, 6, 13)
    bg = Color(212, 8, 18)
    block = False

exported_class = BloodLight
