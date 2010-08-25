import os, pickle, random
from textwrap import wrap
from copy import copy

from pytcod import *

from src.level import Level
from src.scenes import Scene
from src import entities
from src.utils import dlog, dtrace

death_messages = [
    "Ack, stupid bots!",
    "The wrong move!",
    "Ugh, not again!",
    "Damn bucket of bolts!",
    "Blasted tin-head!",
    "Doggone it!",
    "Wretched automaton!"
]

def random_deathmsg():
    return random.choice(death_messages)

class MessageFrame(object):
    def __init__(self, x, y, width, height, message, title):        
        self.x = x - (width/2)
        self.y = y - (height/2)
        self.width = width
        self.height = height
        self.title = title
        self.message = wrap(message, width - 2)
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
        print self.message, self.height, self.nblines, self.maxline
        
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
        if self.line > 0:
            self.view.set_char(self.width - 1, 0, CHAR_ARROW_N)

    def scroll_down(self):
        if self.line < self.maxline:
            self.line += 1
            self._render()
    def scroll_up(self):
        if self.line > 0:
            self.line -= 1
            self._render()

class GameplayScene(Scene):

    first_level = "levelone"

    def __init__(self):
	self.dirty = True
        self.init_prism_palettes()

    def init_prism_palettes(self):
        self.darkprism = []
        self.lightprism = []
        for x in range(25):
            rnd = random.random()
            rndc = Color(random.randint(128, 255), 
                         random.randint(128, 255), 
                         random.randint(128, 255))
            bg = BLACK.lerped(rndc, min(.04,max(.02, rnd)))
            self.darkprism.append(bg)
            rndc = Color(random.randint(128, 255), 
                         random.randint(128, 255), 
                         random.randint(128, 255))
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
        self.playerdead = False

        self.frame = None
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

    def reset(self):
        p = self._player
        self.load(self.levelname)
        self.player = p
        self._player = copy(self.player)
        self.playerdead = False
        self.map.compute_fov(self.player.x, self.player.y)

    def player_death(self, ent):
        self.playerdead = True
        msg = random_deathmsg()
        self.set_frame(self.view.width / 2, 30, 
                       25, 5, 
                       msg, "Wiz says:")

    def set_frame(self, x, y, width, height, message, title):
        self.frame = MessageFrame(x, y, width, height, message, title)        

    def update(self):
	action = self.app.input.check_for_action('game')
	if action:
            if self.frame:
                if action == 'move_down':
                    self.frame.scroll_down()
                elif action == 'move_up':
                    self.frame.scroll_up()
                elif action == 'confirm':
                    self.frame = None
                    if self.playerdead:
                        self.reset()
                self.dirty = True
                return
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
            # Draw ground and FOV
            for x in xrange(view.width):
                for y in xrange(view.height):
                    bg = random.choice(self.darkprism)
                    if self.map.cell(x, y).lit:
                        bg = random.choice(self.lightprism)
                        bg = bg.lerped(YELLOW, .04)
                    view.put_char(x, y, ord(self.ground.icon), self.ground.fg, bg)
            # Draw tiles
            for tile in  self.level.tiles:
                bg = tile.bg.lerped(random.choice(self.lightprism), min(.2, random.random()))
                cell = self.map.cell(tile.x, tile.y)
                if cell.lit:# or tile.name=='stone':
                    self.view.put_char(tile.x, tile.y, ord(tile.icon), tile.fg, bg)
            # Draw Player
            p = self.player
            self.view.set_char(p.x, p.y, ord(p.icon))
            self.view.set_fore(p.x, p.y, p.fg)
            # Draw entities
            for ent in  self.level.entities:
                cell = self.map.cell(ent.x, ent.y)
                if cell.lit:
                    self.view.set_char(ent.x, ent.y, ord(ent.icon))
                    self.view.set_fore(ent.x, ent.y, ent.fg)
            # Draw message frame
            if self.frame:
                v = self.frame.view
                self.view.blit(v, self.frame.x, self.frame.y)
        self.dirty = False
exported_class = GameplayScene
