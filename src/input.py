import string
from ConfigParser import RawConfigParser

import pytcod

from src.utils import dlog

class InputMapper(object):

    keylist = [
        'K_NONE', 'K_ESCAPE', 'K_BACKSPACE', 'K_TAB',
        'K_ENTER', 'K_SHIFT', 'K_CONTROL', 'K_ALT',
        'K_PAUSE', 'K_CAPSLOCK', 'K_PAGEUP', 'K_PAGEDOWN',
        'K_END', 'K_HOME', 'K_UP', 'K_LEFT',
        'K_RIGHT', 'K_DOWN', 'K_PRINTSCREEN', 'K_INSERT',
        'K_DELETE', 'K_LWIN', 'K_RWIN', 'vK_APPS',
        'K_0', 'K_1', 'K_2', 'K_3',
        'K_4', 'K_5', 'K_6', 'K_7',
        'K_8', 'K_9', 'K_KP0', 'K_KP1',
        'K_KP2', 'K_KP3', 'K_KP4', 'K_KP5',
        'K_KP6', 'K_KP7', 'K_KP8', 'K_KP9',
        'K_KPADD', 'K_KPSUB', 'K_KPDIV', 'K_KPMUL',
        'K_KPDEC', 'K_KPENTER', 'K_F1', 'K_F2',
        'K_F3', 'K_F4', 'K_F5', 'K_F6',
        'K_F7', 'K_F8', 'K_F9', 'K_F10',
        'K_F11', 'K_F12', 'K_NUMLOCK', 'K_SCROLLLOCK',
        'K_SPACE', 'K_CHAR',
    ]

    valid_chars = string.printable[:-5]

    def __init__(self, app):
        self.app = app
        self.lastkey = None
        self.parser = RawConfigParser()
        self.parser.optionxform = str
        self.load_mapping()

    def load_mapping(self, filename='userinput.conf'):
        fobj = open('data/input.conf', 'r')
        self.parser.readfp(fobj)
	try: 
	    fobj = open(filename, 'r')
            self.parser.readfp(fobj)
	except IOError:
	    self.parser.write(open("userinput.conf", 'w'))
        valid = True # validate
        for section in self.parser.sections():
            print self.parser.options(section)
            items = self.parser.items(section)
            for key, action in items:
                if not hasattr(pytcod, key) and key not in self.valid_chars:
                    print "{0} - ({1}, {2}): {1} is not a valid key.".format(section, key, action)
                    valid = False
        if not valid:
            raise Exception("Input configuration contains invalid keys.")
        self.section = self.parser.sections()[0]
    
    def check_for_action(self, section):
        key = self.app.window.check_for_key(pytcod.PRESSED)
        self.lastkey = key
        if key.vkey != pytcod.K_CHAR:
            key_name = self.keylist[key.vkey]
        else:
            key_name = chr(key.char)
        if self.parser.has_option(section, key_name):
            return self.parser.get(section, key_name)
        
