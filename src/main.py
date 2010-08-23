import numpy as np
from pytcod import *

CHUNKH = 100
CHUNKW = 100
CHUNKD = 100

EMPTY = 0
STONE = 1

class Position:
    def __init__(self, z, x, y):
        self.z, self.x, self.y = z, x, y

class Chunk:
    def __init__(self):
        self.data = np.zeros((CHUNKH, CHUNKW, CHUNKD), dtype=np.uint8)

    def load(self, filename):
        self.data = np.load(filename + ".npy")
        return self

    def save(self, filename):
        np.save(filename, self.data)
        return self

    def clip(self, zs, ze, xs, xe, ys, ye):
        return self.data[zs : ze, xs : xe, ys : ye]

class Editor:
    def __init__(self):
        self.chunk = Chunk()
        self.position = Position(10, CHUNKW / 2, CHUNKH / 2)
        self.dirty = True

    def save(self, filename):
        self.chunk.save("data/props/" + filename)

    def load(self, filename):
        self.chunk.load("data/props/" + filename)
        self.dirty = True

    def place(self, cell, x, y):
        self.chunk.data[self.position.z - 1, x, y] = cell
        self.dirty = True

    def remove(self, x, y):
        self.chunk.data[self.position.z - 1, x, y] = EMPTY
        self.dirty = True

    def draw(self, view, force=False):
        if not self.dirty and not force:
            return
        self.dirty = False
        
        # Clear to bg color
        view.bg = Color(42, 42, 48)
        view.clear()

        # Clip to view
        hw = view.width / 2
        hh = view.height / 2
        block = self.chunk.clip(0, self.position.z,
                                self.position.x - hw, self.position.x + hw,
                                self.position.y - hh, self.position.y + hh)

        # Draw to view
        for x in range(len(block[0])):
            for y in range(len(block[0][0])):
                for z in range(len(block) - 1, -1, -1):
                    cell = block[z, x, y]
                    if cell == EMPTY:
                        continue
                    fg = (255 / self.position.z - 1) * (z + 2)
                    bg = (128 / self.position.z - 1) * (z + 2)
                    if z == self.position.z - 1:
                        fgc = Color(0, 0, 0)
                    else:
                        fgc = Color(fg, fg, fg)
                    view.put_char(x, y, ord('.'), fgc, Color(bg, bg, bg))
                    break

def main():
    font = Font("data/fonts/lucida12x12_gs_tc.png",
                FONT_GREYSCALE | FONT_TCOD)
    window = Window(80, 50, "Between Roc Peak and Haardeplace", font=font)
    editor = Editor()
    view = Console(80, 50)

    running = True
    while running and not window.is_closed():
        # Clear window
        window.clear()

        # Render editor
        editor.draw(view, True)

        # Draw editor
        window.blit(view)

        # Draw fps
        window.write(str(window.fps))

        # Flip screen
        window.flush()

        # Check key input
        key = window.check_for_key(PRESSED | RELEASED)
        if key.pressed:
            if key.vkey == K_ESCAPE:
                running = False
            elif key.vkey == K_UP:
                editor.position.z += 1
            elif key.vkey == K_DOWN:
                editor.position.z -= 1

        # Check mouse
        mouse = window.mouseinfo
        if mouse.lbutton:
            x = (CHUNKW - view.width) / 2 + mouse.cx
            y = (CHUNKH - view.height) / 2 + mouse.cy
            editor.place(STONE, x, y)
        elif mouse.rpressed:
            x = (CHUNKW - view.width) / 2 + mouse.cx
            y = (CHUNKH - view.height) / 2 + mouse.cy
            editor.remove(x, y)
