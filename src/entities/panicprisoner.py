import random

from pytcod import *
from src.entities import Entity, get


class PanicPrisoner(Entity):
    name = 'panicprisoner'
    icon = "P"
    fg = YELLOW
    block = True
    path = None
    stun = 0
    
    def update(self, game):
        level = game.level
        player = game.player
        map = game.map
        map.compute_fov(self.x, self.y, radius=10, walls=False)
        playercell = map.cell(player.x, player.y)
        if playercell.lit:
            actions = []
            if player.x > self.x:
                actions.append(self.move_right)
            elif player.x < self.x:
                actions.append(self.move_left)
            if player.y > self.y:
                actions.append(self.move_down)
            elif player.y < self.y:
                actions.append(self.move_up)
            for action in actions:
                action(game)

exported_class = PanicPrisoner
