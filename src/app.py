from ConfigParser import RawConfigParser

from src.input import InputMapper
from src.utils import *
from src.materials import MaterialsManager

from pytcod import *

class Configuration(RawConfigParser):

    _defaultconf = "data/options.conf"

    def __init__(self, filename=_defaultconf):
        RawConfigParser.__init__(self)

        fobj = open(self._defaultconf)
        self.readfp(fobj)
        try:
            fobj = open(filename, 'r')
            self.readfp(fobj)
        except IOError:
            self.write(open("useroptions.conf", 'w'))

    def get(self, section, *args):
        if len(args) == 1:
            return RawConfigParser.get(self, section, *args)
        else:
            options = []
            for arg in args:
                o = RawConfigParser.get(self, section, arg)
                options.append(o)
            return options

class Application(object):
    
    def __init__(self):
        self.conf = Configuration("useroptions.conf")
        w, h = self.conf.get('core', 'window_width', 'window_height')
        font_file = self.conf.get('render', 'font_file')
        font = Font(font_file, FONT_GREYSCALE | FONT_TCOD)
        dlog("{0},{1}, {2}".format(w, h, font_file))
        self.window = Window(int(w), int(h), "Prison Break", font=font)
        self.window.keyrepeat = (100, 100)
        self.view = Console(int(w), int(h))
        self.input = InputMapper(self)

        self._scene = None
        self.running = False

    def _get_scene(self):
        return self._scene

    def _set_scene(self, scene):
        if self._scene:
            self._scene.leave()
        scene.enter(self)
        self._scene = scene
    scene = property(_get_scene, _set_scene)

    def check_for_action(self, section):
        return self.input.check_for_action(section)

    def run(self, scene):
        self.running = True
        self.scene = scene
        while self.running and not self.window.is_closed():
            self.window.clear()
            self.scene.draw(self.view, False)
            self.window.blit(self.view)
            self.window.write("{0}/fps".format(self.window.fps))
            self.window.flush()

            self.scene.update()

        self.window = None
