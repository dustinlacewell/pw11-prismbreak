import os, pickle
import numpy as np

from pytcod import Color

from src import entities
from src.scenes import Scene
from src.utils import dlog, dtrace
from src.imports import get_all

class Level(object):

    def __init__(self, app):
        self.w = app.view.width
        self.h = app.view.height

        self.tiles = []
        self.entities = []

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

    def build(self, x, y, etype):
        ct = self.level.tile_at(x, y)
        if ct:
            self.destroy(ct)
        self.level.tiles.append(etype(x, y))

    def place(self, x, y, etype):
        ce = self.level.ent_at(x, y)
        if ce:
            self.remove(ce)
        self.level.entities.append(etype(x, y))

    def destroy(self, entity):
        if entity in self.level.tiles:
            self.level.tiles.remove(entity)

    def remove(self, entity):
        if entity in self.level.entities:
            self.level.entities.remove(entity)
        
    def reset_editor(self):
        self.mode = 't'
        self.mark = None
        self.delmark = None

    def next_brush(self):
        self.palette.append(self.palette.pop(0))

    def prev_brush(self):
        self.palette.insert(0, self.palette.pop())

    def _getbrush(self):
        return self.palette[0]
    brush = property(_getbrush)

    def save(self, filename):
        print os.getcwd()
        fobj = open(os.path.join("data/levels", filename + '.lvl'), 'w')
        pickle.dump(self.level, fobj)
        print "Level '{0}' saved".format(filename)

    def load(self, filename):
        try:
            fobj = open(os.path.join("data/levels", filename + '.lvl'), 'r')
            self.level = pickle.load(fobj)
            self.reset_editor()
            self.dirty = True
            print "Level '{0}' loaded".format(filename)
        except:
            print "Unable to load '{0}'".format(filename)

    def update(self):
	action = self.app.input.check_for_action('editor')
	if action:
	    if action == 'quit':
		self.app.running = False
            elif action == 'tile_mode':
                print "TILE MODE"
                self.mode = 't'
            elif action == 'ent_mode':
                print "ENTITY MODE"
                self.mode = 'e'
            elif action == 'next_brush':
                self.next_brush()
                print "CURRENT BRUSH:", self.brush.name
            elif action == 'prev_brush':
                self.prev_brush()
                print "CURRENT BRUSH:", self.brush.name
            elif action == 'save':
                s = raw_input("Level name:")
                self.save(s)
            elif action == 'load':
                s = raw_input("Level name:")
                self.load(s)

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
                method = self.build if self.mode == 't' else self.place
                for ix in xiter:
                    for iy in yiter:
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
                method = self.destroy if self.mode == 't' else self.remove
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
            self.view.set_char(ent.x, ent.y, ord(ent.icon))
            self.view.set_fore(ent.x, ent.y, ent.fg)
        if self.mark:
            mx, my = self.mark
            self.view.put_char(mx, my, ord(self.markmat.icon), self.markmat.fg, self.markmat.bg)
        if self.delmark:
            mx, my = self.delmark
            self.view.put_char(mx, my, ord(self.markmat.icon), self.markmat.bg, self.markmat.fg)

exported_class = EditorScene
