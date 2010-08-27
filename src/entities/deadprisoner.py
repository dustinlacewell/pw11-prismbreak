from pytcod import *
from src.entities import Entity


class DeadPrisoner(Entity):
    name = 'deadprisoner'
    icon = "p"
    fg = LIGHT_GRAY
    bg = Color(212, 8, 18)
    block = False

exported_class = DeadPrisoner
