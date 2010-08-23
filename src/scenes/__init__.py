from src import imports

def get( command_name ):
    """Return the command class for the given command-name."""
    return imports.get('scenes', command_name)

class Scene(object):
    def update(self):
        pass
    def enter(self):
        pass
    def leave(self):
        pass
