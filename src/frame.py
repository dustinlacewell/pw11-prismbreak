from textwrap import wrap

from pytcod import *

class MessageFrame(object):
    def __init__(self, x, y, width, height, message, title,wrapped=True):        
        self.x = x - (width/2)
        self.y = y - (height/2)
        self.width = width
        self.height = height
        self.title = title
        if wrapped:
            self.message = wrap(message, width - 2, drop_whitespace = False)
        else:
            self.message = message
        self.nblines = len(self.message)
        self.line = 0
        if self.nblines <= height - 2:
            self.maxline = 0
        else:
            self.maxline = self.nblines - (self.height - 2)

        self.view = Console(width, height)
        self.view.bg = BLACK
        self.view.fg = WHITE
        self._render()
        
    def _render(self):
        self.view.clear()
        nl = self.line
        for i in range(1, self.height - 1):
            self.view.write(self.message[nl], 1, i, align=LEFT)
            nl += 1
            if nl == self.nblines:
                break
        self.view.print_frame(0, 0, self.width, self.height, self.title, empty=False)
        if self.line < self.maxline:
            self.view.set_char(self.width - 1, self.height - 1, CHAR_ARROW_S)
            self.view.set_fore(self.width - 1, self.height - 1, RED)
        if self.line > 0:
            self.view.set_char(self.width - 1, 0, CHAR_ARROW_N)
            self.view.set_fore(self.width - 1, 0, RED)

    def scroll_down(self):
        if self.line < self.maxline:
            self.line += 1
            self._render()
    def scroll_up(self):
        if self.line > 0:
            self.line -= 1
            self._render()

