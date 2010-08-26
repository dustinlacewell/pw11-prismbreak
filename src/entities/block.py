from pytcod import *

from src.entities import Entity


class Block(Entity):
    name = 'block'
    type = 'wall'
    icon = chr(CHAR_CHECKBOX_UNSET)
    fg = Color(90, 104, 110)
    bg = Color(73,58,67)
    block = True
    transparent = False

exported_class = Block
