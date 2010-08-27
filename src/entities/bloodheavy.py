from pytcod import *
from src.entities import Entity


class BloodHeavy(Entity):
    name = 'bloodheavy'
    icon = chr(CHAR_BLOCK3)
    fg = Color(162, 6, 13)
    bg = Color(212, 8, 18)
    block = False

exported_class = BloodHeavy
