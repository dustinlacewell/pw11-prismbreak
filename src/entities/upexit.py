from pytcod import *

from src.entities import Entity


class UpExit(Entity):
    name = 'upexit'
    icon = "^"
    bg = Color(0, 0, 0)
    fg = Color(153, 182, 196)
    block = True

exported_class = UpExit
