from pytcod import *
from src.entities import Entity


class BloodMed(Entity):
    name = 'bloodmed'
    icon = chr(CHAR_BLOCK2)
    fg = Color(162, 6, 13)
    bg = Color(212, 8, 18)
    block = False

exported_class = BloodMed
