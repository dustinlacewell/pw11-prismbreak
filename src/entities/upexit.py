from pytcod import *

from src.entities import exitbase


class UpExit(exitbase.Exit):
    name = 'upexit'
    icon = "["
    bg = Color(0, 0, 0)
    fg = Color(153, 182, 196)

exported_class = UpExit
