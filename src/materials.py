from ConfigParser import RawConfigParser
from pytcod import *

from src.utils import dlog

class Material(object):
    name = "none"
    icon = "X"
    _fg = Color(0, 0, 255)
    _bg = Color(255, 0 ,0)

    def __init__(self, conf):
	self.conf = conf
	self.fg = self._fg
	self.bg = self._bg

    def _get_fg(self):
	return self._fg
    def _set_fg(self, c):
	self._fg = c
    fg = property(_get_fg, _set_fg)

    def _get_bg(self):
	return self._bg
    def _set_bg(self, c):
	self._bg = c
    bg = property(_get_bg, _set_bg)

    def __cmp__(self, other):
	return hash(self) == hash(other)

    def __hash__(self):
	return hash(self.name)

class MaterialsManager(object):

    def __init__(self, app, conf="data/materials.conf"):
	self.app = app
	self.parser = RawConfigParser()
	self.materials = {}
	self.parse_conf(conf)

    def clear_all(self):
	self.materials.clear()

    def parse_conf(self, conf):
	p = self.parser
	p.read([conf])
	for section in p.sections():
	    newmat = Material(self.app.conf)
	    newmat.name = section
	    newmat.icon = " "
	    if p.has_option(section, 'icon'):
		newmat.icon = p.get(section, 'icon')[0]
	    # parse colors
	    try:
		fg = [int(c) for c in p.get(section, 'fg').split(',')]
		bg = [int(c) for c in p.get(section, 'bg').split(',')]
	    except:
		dlog("Couldn't parse color in '{0}', skipping...")
		if not self.materials.get(section):
		    self.materials[section] = Material()
		continue
	    
	    newmat.fg = Color(*fg)
	    newmat.bg = Color(*bg)
	    self.materials[section] = newmat

    def __getitem__(self, key):
	# empty hash
	if key == 0:
	    return Material(self.app.conf)
	# hash
	if type(key) != type(' '):
	    for mat in self.materials.itervalues():
		if hash(mat) == key:
		    return mat
	# name
	mat = self.materials.get(key)
	# not found
	if not mat:
	    mat = Material(self.app.conf)
	return mat
