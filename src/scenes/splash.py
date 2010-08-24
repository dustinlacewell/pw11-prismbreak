from pytcod import *

from src import scenes

from src.utils import dlog

class SplashScene(scenes.Scene):
    def __init__(self):
	self.image = Image.load("data/images/splash.png")

    def enter(self, app):
	self.app = app
	self.view = app.view

    def update(self):
	action = self.app.input.check_for_action('editor')
	if action:
	    if action == 'quit':
		self.app.running = False
	if self.app.input.lastkey.vkey != K_NONE and action !='quit' :
	    scene = scenes.get('game')()
	    self.app.scene = scene

    def draw(self, view, force=False):
        # Clear to bg color
        view.bg = Color(42, 42, 48)
	view.fg = WHITE
	view.bliti_2x(self.image, 0, 0)

exported_class = SplashScene
