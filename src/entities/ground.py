from pytcod import *
from src.entities import Entity


class Ground(Entity):
    name = 'ground'
    icon = "."
    fg = Color(42, 45, 50)
    bg = Color(31, 33, 37)
    block = False

exported_class = Ground
