import random
from copy import copy

from pytcod import *
from src.entities import Entity


class Player(Entity):
    name = 'player'
    type = 'player'
    icon = "W"
    fg = Color(100, 63, 161)
    bg = Color(31, 33, 37)
    staff = False
    masterkey = False
    scrap = 0
    keys = 0

    guard_messages = [
        "Ack, stupid bots!",
        "The wrong move!",
        "Ugh, not again!",
        "Damn bucket of bolts!",
        "Blasted tin-head!",
        "Doggone it!",
        "Wretched automaton!"
    ]

    electricity_messages = [
        "You were zapped!",
        "Yeah I should probably avoid the live electricity.",
        "Who thought live wires were dangerous?",
        "Note to self: don't touch power lines",
    ]

    

    def touched(self, game, ent):
        if ent.type == 'guard':
            game.player_death(ent)
        if ent.name == 'masterguard' and not self.staff:
            game.set_frame(40, 3, "I don't think I can beat him without magic. He's just to darned fast.", "Wizard grumbles:")


    def random_deathmsg(self, game, ent):
        name = "%s_messages" % ent.type
        if hasattr(self, name):
            msg = random.choice(getattr(self, name))
            return msg
        return "ACK!"
        
        

exported_class = Player
