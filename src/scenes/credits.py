
from pytcod import *

from src.scenes import Scene, get
from src.frame import MessageFrame

class CreditsScene(Scene):

    def enter(self, app):
	self.app = app
	self.view = app.view

	self.dirty = True
	lastmsg = [
	    "",
	    "Yessir! Escaped I have, it seems!",
	    "",
	    "Now onto that Amulet of Yendor!",
	    "",
	    "Oh it sure is lovely to see",
	    "a tree again..."
	    ]

	self.lastmsg = MessageFrame(self.view.width / 2, self.view.height / 2,
				    40, 10,
	                            lastmsg, "Wizard exclaims:",
				    wrapped=False)
	credits = [
	    "",
	    "          Special thanks goes to,",
	    "",
	    "            ajhager & _habnabit,",
            "",
	    "for their help getting the game packaged.",
	    "",
	    "            yay for pyweek \o/",
            "",
            "           ~  Dustin  Lacewell",]
	self.credits = MessageFrame(self.view.width / 2, self.view.height / 2,
				    44, len(credits) + 3,
				    credits, "Thanks for playing my game!",
				    wrapped = False)

	self.frame = self.lastmsg
	self._frame = 0
	self.oldx = self.view.width / 2
	self.oldy = self.view.height / 2
	self.view.bg = BLACK

    def update(self):
	mouse = self.app.window.mouseinfo
	action = self.app.input.check_for_action('game')
	if action:
	    if self._frame == 0:
		print "wtf"
		self.frame == self.credits
		self._frame += 1
		self.dirty = True
	    elif self._frame == 1:
		print "no clue"
		self._frame += 1
		self.app.scene = get('splash')()
		self.dirty = True

    def draw(self, view, force=False):
	if self.dirty:
	    self.view.clear()
	    if self._frame == 0:
		v = self.lastmsg.view
	    else:
		v = self.credits.view
	    self.view.blit(v, self.frame.x, self.frame.y)
	    self.dirty = False

exported_class = CreditsScene	
				    
 
