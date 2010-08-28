
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
            "        ajhager, _habnabit & cortesi",
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
        self.cx = 79
        self.cy = 0
        self.view.bg = BLACK
        self.colors = Color.gradient({1:RED, 50:GREEN, 100:BLUE, 150:RED})

    def update(self):
	self.nextc()
	self.dirty = True
        mouse = self.app.window.mouseinfo
#	if (self.cx, self.cy) != (mouse.cx, mouse.cy):
#	    self.dirty = True
#	    self.cx, self.cy = mouse.cx, mouse.cy
#	print self.cx, self.cy
        action = self.app.input.check_for_action('game')
        if action:
            if self._frame == 0:
                self.frame == self.credits
                self._frame += 1
                self.dirty = True
            elif self._frame == 1:
                self._frame += 1
                self.app.scene = get('splash')()
                self.dirty = True
    def nextc(self):
	c = self.colors.pop()
	self.colors.insert(0, c)
	return c

    def draw(self, view, force=False):
        if self.dirty:
            self.view.clear()
            for i in range(0, self.view.width - 1):
                for _x, _y in Line(i, 0, self.cx, self.cy):
                    self.view.put_char(_x, _y, ord("*"), fg=self.nextc())
                for _x, _y in Line(i, self.view.height - 1, self.cx, self.cy):
                    self.view.put_char(_x, _y, ord("*"), fg=self.nextc())

            for i in range(0, self.view.height - 1):
                for _x, _y in Line(0, i, self.cx, self.cy):
                    self.view.put_char(_x, _y, ord("*"), fg=self.nextc())
                for _x, _y in Line(self.view.height - 1, i, self.cx, self.cy):
                    self.view.put_char(_x, _y, ord("*"), fg=self.nextc())

            if self._frame == 0:
                v = self.lastmsg.view
            else:
                v = self.credits.view
            self.view.blit(v, self.frame.x, self.frame.y)
            self.dirty = False

exported_class = CreditsScene   
                                    
 
