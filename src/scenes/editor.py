import numpy as np

from pytcod import Color

from src import entities
from src.scenes import Scene
from src.utils import dlog, dtrace
from src.imports import get_all

class Level(object):

    def __init__(self, app):
        self.app = app
        self.w = app.view.width
        self.h = app.view.height

        self.tiles = []
        self.entities = []

    def build(self, x, y, etype):
        self.tiles.append(etype(x, y, self.app, self))

    def place(self, x, y, etype):
        self.entities.append(etype(x, y, self.app, self))

    def destroy(self, entity):
        if entity in self.tiles:
            self.tiles.remove(entity)

    def remove(self, entity):
        if entity in self.entities:
            self.entities.remove(entity)
        
    def tile_at(self, x, y):
        print 'tileat', x, y
        for t in self.tiles:
            if t.x == x and t.y == y:
                return t

    def ent_at(self, x, y):
        for e in self.entities:
            if e.x == x and e.y == y:
                return e

    def draw(self):
        pass


class EditorScene(Scene):
    def __init__(self):
	self.dirty = True

    def enter(self, app):
	self.app = app
	self.view = app.view
        
        self.palette = [ ]
        for name  in get_all('entities'):
            newtype = entities.get(name)
            self.palette.append(newtype)
            
        self.level = Level(app)

        self.mode = 't'
        self.mark = None
        self.delmark = None
        self.markmat = entities.get('mark')

    def next_brush(self):
        self.palette.append(self.palette.pop(0))

    def prev_brush(self):
        self.palette.insert(0, self.palette.pop())

    def _getbrush(self):
        return self.palette[0]
    brush = property(_getbrush)

    def save(self, filename):
        pass

    def load(self, filename):
        pass

    def update(self):
	action = self.app.input.check_for_action('editor')
	if action:
	    if action == 'quit':
		self.app.running = False
            elif action == 'tile_mode':
                self.mode = 't'
            elif action == 'ent_mode':
                self.mode = 'e'
            elif action == 'next_brush':
                self.next_brush()
            elif action == 'prev_brush':
                self.prev_brush()

	mouse = self.app.window.mouseinfo
        if mouse.mpressed:
            if not self.mark:
                self.mark = (mouse.cx, mouse.cy)
                self.dirty = True
            else:
                w = mouse.cx - self.mark[0]
                h = mouse.cy - self.mark[1] 
                if w >= 0:
                    xiter = xrange(w + 1)
                else:
                    xiter = xrange(w, 1, 1)
                if h >= 0:
                    yiter = xrange(h + 1)
                else:
                    yiter = xrange(h, 1, 1)
                method = self.level.build if self.mode == 't' else self.level.place
                for ix in xiter:
                    for iy in yiter:
                        print "Placing", ix, iy, self.mark[0] + ix, self.mark[1] + iy
                        method(self.mark[0] + ix, self.mark[1] + iy, self.brush)
                self.dirty = True
                self.mark = None
        if mouse.rpressed:
            if not self.delmark:
                self.delmark = (mouse.cx, mouse.cy)
                self.dirty = True
            else:
                w = mouse.cx - self.delmark[0]
                h = mouse.cy - self.delmark[1] 
                if w >= 0:
                    xiter = xrange(w + 1)
                else:
                    xiter = xrange(w, 1, 1)
                if h >= 0:
                    yiter = xrange(h + 1)
                else:
                    yiter = xrange(h, 1, 1)
                method = self.level.destroy if self.mode == 't' else self.level.remove
                method2 = self.level.tile_at if self.mode == 't' else self.level.ent_at
                for ix in xiter:
                    for iy in yiter:
                        print "Destroying", ix, iy, self.delmark[0] + ix, self.delmark[1] + iy
                        ent = method2(self.delmark[0] + ix, self.delmark[1] + iy)
                        method(ent)
                self.dirty = True
                self.delmark = None

    def draw(self, view, force=False):
        if not self.dirty and not force:
            return
        self.dirty = False
        
        # Clear to bg color
        self.view.bg = Color(42, 42, 48)
        self.view.clear()

        for tile in  self.level.tiles:
            self.view.put_char(tile.x, tile.y, ord(tile.icon), tile.fg, tile.bg)
        for ent in  self.level.entities:
            self.view.put_char(ent.x, ent.y, ord(ent.icon), ent.fg, ent.bg)
        if self.mark:
            mx, my = self.mark
            self.view.put_char(mx, my, ord(self.markmat.icon), self.markmat.fg, self.markmat.bg)
        if self.delmark:
            mx, my = self.delmark
            self.view.put_char(mx, my, ord(self.markmat.icon), self.markmat.bg, self.markmat.fg)

exported_class = EditorScene
