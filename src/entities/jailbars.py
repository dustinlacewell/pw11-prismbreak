from pytcod import *
from src.entities import Entity


class Jailbars(Entity):
    name = 'jailbars'
    type = 'wall'
    icon = "="
    fg = Color(197, 166, 184)
    bg = Color(31, 33, 37)
    block = True
    transparent = True

exported_class = Jailbars
