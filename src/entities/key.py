from pytcod import *

from src.entities import Entity


class Key(Entity):
    name = 'key'
    icon =  '{'
    fg = YELLOW

    def touched(self, game, ent):
        if ent.name == 'player':
            game.player.keys += 1
            game.remove(self)
            if 'KEYMESSAGE' not in game.seenmsgs:
                game.seenmsgs.add('KEYMESSAGE')
                game.set_frame(20, 3,
                               "You aquired a key.",
                               "Note:")

exported_class = Key
