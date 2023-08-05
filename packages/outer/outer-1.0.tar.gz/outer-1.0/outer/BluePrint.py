from outer.VirtualTerminal import VirtualTerminal
from outer.File import File


class BluePrint:
    def __init__(self):
        self._root_dir = 'log'
        # default to init
        self.init()

    def init(self, root_dir='log'):
        self._root_dir = root_dir
        terminal = VirtualTerminal(root=root_dir)
        # set terminal
        for name, obj in vars(self).items():
            if type(obj) is File:
                obj.set_terminal(terminal)
        return self