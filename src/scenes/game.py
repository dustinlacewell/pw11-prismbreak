import os, pickle, random
from copy import copy

from pytcod import *

from src.level import Level
from src.scenes import Scene
from src import entities
from src.utils import dlog, dtrace

class GameplayScene(Scene):

    first_level = "levelone"

    def __init__(self):
	self.dirty = True
        self.darkprism = []
        self.lightprism = []
        for x in range(25):
            rnd = random.random()
            rndc = Color(random.randint(128, 255), random.randint(128, 255), random.randint(128, 255))
            bg = BLACK.lerped(rndc, min(.04,max(.02, rnd)))
            self.darkprism.append(bg)
            rndc = Color(random.randint(128, 255), random.randint(128, 255), random.randint(128, 255))
            bg = BLACK.lerped(rndc, min(.07,max(.04, rnd)))
            self.lightprism.append(bg)
            

    def enter(self, app):
	self.app = app
	self.view = app.view
        
        self.ground = entities.get('ground')
        self.map = None
        self.levelname = 'start'
        sx, sy = self.load(self.first_level)

        self.player = entities.get('player')(sx, sy)
        self._player = copy(self.player)

        self.dirty = True

    def remove(self, entity):
        if entity in self.level.entities:
            self.level.entities.remove(entity)

    def add(self, entity):
        self.level.entities.append(entity)

    def load(self, filename):
        try:
            fobj = open(os.path.join("data/levels", filename + '.lvl'), 'r')
            self.level = pickle.load(fobj)
            if self.levelname in self.level.links:
                print self.level.links, self.levelname, filename
                sx, sy = self.level.links[self.levelname]
                self.levelname = filename
                self.map = Map(self.app.view.width, self.app.view.height)
                self.map.clear(transparent=True, walkable=True)
                self.map.radius = int(self.app.conf.get('game', 'wiz_fov'))
                self.map.lightwalls = True
                for tile in self.level.tiles:
                    cell = self.map.cell(tile.x, tile.y)
                    cell.walkable = tile.block
                    cell.transparent = tile.transparent
                self.map.compute_fov(sx, sy)
                return sx, sy
        except Exception, e:
            print e, e.message
            
#        except:
#            print "Unable to load '{0}'".format(filename)

    def update(self):
	action = self.app.input.check_for_action('game')
	if action:
            self.dirty = True
	    if action == 'quit':
		self.app.running = False
                return
            elif action == 'load':
                s = raw_input("Level name:")
                self.load(s)
                return
            elif action.startswith('move'):
                oldx, oldy = self.player.x, self.player.y
                if hasattr(self.player, action):
                    func = getattr(self.player, action)
                    func(self)
                    if (oldx, oldy) != (self.player.x, self.player.y):
                        for entity in self.level.entities:
                            entity.update(self)

            self.map.compute_fov(self.player.x, self.player.y)
	mouse = self.app.window.mouseinfo

    def draw(self, view, force=False):
        if self.dirty:
        # Clear to bg color
            self.view.clear_ex(0, 0,
                               self.view.width, self.view.height, 
                               ord(self.ground.icon), 
                               self.ground.fg, self.ground.bg)

            for x in xrange(view.width):
                for y in xrange(view.height):
                    bg = random.choice(self.darkprism)
                    if self.map.cell(x, y).lit:
                        bg = random.choice(self.lightprism)
                        bg = bg.lerped(YELLOW, .04)
                    view.put_char(x, y, ord(self.ground.icon), self.ground.fg, bg)
                    
            for tile in  self.level.tiles:
                bg = tile.bg.lerped(random.choice(self.lightprism), min(.2, random.random()))
                cell = self.map.cell(tile.x, tile.y)
                if cell.lit:# or tile.name=='stone':
                    self.view.put_char(tile.x, tile.y, ord(tile.icon), tile.fg, bg)
            for ent in  self.level.entities:
                cell = self.map.cell(ent.x, ent.y)
                if cell.lit:
                    self.view.set_char(ent.x, ent.y, ord(ent.icon))
                    self.view.set_fore(ent.x, ent.y, ent.fg)
            p = self.player
            self.view.set_char(p.x, p.y, ord(p.icon))
            self.view.set_fore(p.x, p.y, p.fg)
        self.dirty = False
exported_class = GameplayScene
