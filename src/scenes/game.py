import os, pickle, random, operator
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
        print self.message
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
        self.deadguards = set()
        self.killedguards = set()
        self.seenmsgs = set()
        self.opendoors = set()
        self.keys = 0

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
        self.lastlevel = 'start'
        sx, sy = self.load(self.first_level)

        self.player = entities.get('player')(sx, sy)
        self._player = copy(self.player)
        self.playerdead = False
        self.casting = None
        self.castline = None
        self.mouse = None
        self.frame = None
        self.lastmouse = None
        self.dirty = True

        self.show_story()

    def remove(self, entity):
        if entity.type == 'guard' and entity.uuid not in self.killedguards:
            self.killedguards.add(entity.uuid)
        if entity in self.level.entities:
            self.level.entities.remove(entity)

    def add(self, entity):
        self.level.entities.append(entity)

    def load(self, filename, reset=False):
        if not reset:
            for guard in self.killedguards:
                self.deadguards.add(guard)
        self.killedguards = set()
        try:
            fobj = open(os.path.join("data/levels", filename + '.lvl'), 'r')
            self.level = pickle.load(fobj)
            self.levelname = filename
            print "LOAD,", filename, "LASTLEVEL", self.lastlevel
            if self.lastlevel in self.level.links:
                sx, sy = self.level.links[self.lastlevel]
                self.map = Map(self.app.view.width, self.app.view.height)
                self.map.clear(transparent=True, walkable=True)
                self.map.radius = int(self.app.conf.get('game', 'wiz_fov'))
                self.map.lightwalls = True
                for tile in self.level.tiles:
                    cell = self.map.cell(tile.x, tile.y)
                    cell.walkable = not tile.block
                    cell.transparent = tile.transparent
                remove = []
                for ent in self.level.entities:
                    if ent.type == 'guard' and ent.uuid in self.deadguards:
                        remove.append(ent)
                for guard in remove:
                    self.level.entities.remove(guard)
                self.map.compute_fov(sx, sy)
                return sx, sy
        except Exception, e:
            print e, e.message
#        except:
#            print "Unable to load '{0}'".format(filename)

    def reset(self):
        p = self._player
        print 'self.levelname', self.levelname
        ppos = self.load(self.levelname, reset=True)
        if ppos:
            p.x, p.y = ppos
        self.player = p
        self._player = copy(self.player)
        self.playerdead = False
        for door in self.opendoors:
            self.opendoor(door, locked=True)
        self.map.compute_fov(self.player.x, self.player.y)

    def player_death(self, ent):
        self.playerdead = True
        msg = random_deathmsg()
        self.set_frame(25, 5, msg, "Wiz says:")

    def set_frame(self, width, height, message, title, wrapped=True):
        x = self.view.width / 2
        y = self.view.height / 2
        self.frame = MessageFrame(x, y, width, height, message, title, wrapped)        

    def resetdoors(self):
        for ent in self.level.entities:
            if ent.name == 'door':
                ent.icon = "+"
                ent.block = True
                ent.transparent = True
                self.map.set_properties(ent.x, ent.y, walkable = False, transparent=False)                    

    def opendoor(self, uuid, locked=False):
        if locked:
            removed = []
            for entity in self.level.entities:
                if entity.name == 'lockeddoor' and entity.uuid == uuid:
                    removed.append(entity)
            for ent in removed:
                self.level.entities.remove(ent)
            if uuid not in self.opendoors:
                self.opendoors.add(uuid)
                return True
        else:
            for ent in self.level.entities:
                if ent.name == 'door' and ent.uuid == uuid:
                    ent.icon = " "
                    ent.block = False
                    print "DOOR UnLOCK", ent, ent.block
                    ent.transparent = True
                    self.map.set_properties(ent.x, ent.y, walkable = True, transparent=True)
                    self.map.compute_fov(self.player.x, self.player.y)


    def show_story(self):
        story = [
            "",
            " Dearly beloved wife,",
            "",
            " I send you this message through mystic",
            " channels to inform you that I have",
            " been delayed in my travels.",
            "",
            " On my way to the dungeon rumored to",
            " hold the prized Amulet of Yendor, I",
            " took camp among some orchards to the",
            " west of the Narathar Banks. At night",
            " I was caught flatfooted by a troupe",
            " of magic hating bots from the",
            " League of the Robotguard.",
            "",
            " The bots have imprisoned me in their",
            " magic-nullifying gulag known as the",
            " Prismguard.",
            "",
            " I will attempt my escape and return",
            " post-haste to the task at hand. My",
            " travels have certainly been delayed",
            " but trust that I long to return to you",
            " at once.",
            "",
            " Your grey-bearded love,",
            " Wizard."
            ]
        self.set_frame(48, 30, story, "And the story goes...", False)
        self.dirty = True
       
        
    def show_help(self):
        help = [
            "How to play:",
            " 1. Escape Prismguard.",
            " 2. Avoid the robots.",
            " 3. If two robots collide, they will drop",
            "    some scrap. You might need it later on.",
            " ",
            "Move:        Arrow Keys",
        ]

        self.set_frame(32, 9, help, "Prism Break Help", False)
        self.dirty = True

    def check_teleport(self, cell):
        for ent in self.level.entities:
            if ent.x == cell.x and ent.y == cell.y and ent.block:
                return None
        if cell.lit and cell.walkable:
            return Line(self.player.x, self.player.y, cell.x, cell.y)

    def check_block(self, cell):
        for ent in self.level.entities:
            if ent.x == cell.x and ent.y == cell.y:
                return None
        if cell.lit and cell.walkable:
            return Line(self.player.x, self.player.y, cell.x, cell.y)

    def check_stun(self, cell):
        for ent in self.level.entities:
            if ent.x == cell.x and ent.y == cell.y and ent.type == 'guard':
                return Line(self.player.x, self.player.y, ent.x, ent.y)

    def cast_teleport(self, cell):
        self.player.do_move(self, cell.x, cell.y)
        return True

    def cast_block(self, cell):
        block = entities.get('block')
        self.level.entities.append(block(cell.x, cell.y))
        self.map.set_properties(cell.x, cell.y, 
                                transparent=block.transparent,
                                walkable=block.block)
        return True

    def cast_stun(self, cell):
        ent = self.level.ent_at(cx, cy)
        ent.stun += 2
        ent.set_path(self)
        return True

    def update(self):
	self.mouse = self.app.window.mouseinfo
        action = self.app.input.check_for_action('game')
        oldx, oldy = self.player.x, self.player.y
        

        if self.casting:
            cx, cy = self.mouse.cx, self.mouse.cy
            if (cx, cy) != self.lastmouse:
                self.lastmouse = (cx, cy)
                mcell = self.map.cell(cx, cy)
                checkname = 'check_%s' % self.casting
                if hasattr(self, checkname):
                    checker = getattr(self, checkname)
                    self.castline = checker(mcell)
                    self.dirty = True
            if self.mouse.lpressed and self.castline:
                castname = "cast_%s" % self.casting
                castcell = self.map.cell(cx, cy)
                if hasattr(self, castname):
                    caster = getattr(self, castname)
                    if caster(castcell):
                        self.update_entities()
                        self.casting = None
                        self.castline = None
                        self.map.compute_fov(self.player.x, self.player.y)
                        self.dirty = True
            if action == "quit":
                self.casting = None
                self.castline = None
                self.dirty = True
        elif action:
            if self.frame:
                if action == 'move_down':
                    self.frame.scroll_down()
                elif action == 'move_up':
                    self.frame.scroll_up()
                elif action:
                    self.frame = None
                    if self.playerdead:
                        self.reset()
                self.dirty = True
                return
	    if action == 'quit':
		self.app.running = False
                return
            elif action == 'load':
                s = raw_input("Level name:")
                self.load(s)
                return
            elif action == 'help':
                self.show_story()
            elif action == 'wait':
                self.casting = 'block' #self.update_entities()
            elif action.startswith('move'):
                if hasattr(self.player, action):
                    func = getattr(self.player, action)
                    func(self)
        if (oldx, oldy) != (self.player.x, self.player.y):
            self.map.compute_fov(self.player.x, self.player.y)
            self.update_entities()
            self.dirty = True
        self.map.compute_fov(self.player.x, self.player.y)


    def update_entities(self):
        self.resetdoors()

        active = []
        for entity in self.level.entities:
            if entity.type == 'guard':
                entity.update_path(self)
                if entity.path:
                    active.append(entity)
                    active.sort(key=operator.methodcaller('pathlength'))
                    active.reverse()
        for bot in active:
            if bot in self.level.entities:
                bot.update(self)
        for entity in self.level.entities:
            if entity.type != 'guard':
                entity.update(self)
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
                if tile.type in ['invis']:
                    continue
                bg = tile.bg.lerped(random.choice(self.lightprism), min(.2, random.random()))
                cell = self.map.cell(tile.x, tile.y)
                if cell.lit:# or tile.name=='stone':
                    self.view.put_char(tile.x, tile.y, ord(tile.icon), tile.fg, bg)
            # Draw entities
            for ent in  self.level.entities:
                if ent.type in ['invis']:
                    continue
                cell = self.map.cell(ent.x, ent.y)
                if cell.lit:
                    self.view.set_char(ent.x, ent.y, ord(ent.icon))
                    self.view.set_fore(ent.x, ent.y, ent.fg)
            # Draw Player
            if not self.playerdead:
                p = self.player
                self.view.set_char(p.x, p.y, ord(p.icon))
                self.view.set_fore(p.x, p.y, p.fg)
            # Draw message frame
            if self.frame:
                v = self.frame.view
                self.view.blit(v, self.frame.x, self.frame.y)
            if self.castline:
                castline = list(self.castline)
                for x, y in castline:
                    cell = self.map.cell(x, y)
                    if cell.lit and cell.walkable:
                        bg = self.view.get_back(x, y)
                        bg = bg.lerped(RED, .1)
                        self.view.set_back(x, y, bg)
                bg = self.view.get_back(x, y)
                bg = bg.lerped(RED, .3)
                self.view.set_back(x, y, bg)
        self.dirty = False
exported_class = GameplayScene
