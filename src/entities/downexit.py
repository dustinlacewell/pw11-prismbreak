from pytcod import *

from src.entities import exitbase

class DownExit(exitbase.Exit):
    name = 'downexit'
    icon = "v"
    bg = Color(0, 0, 0)
    fg = Color(153, 182, 196)

exported_class = DownExit
