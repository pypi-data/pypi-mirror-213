import numpy as np

from ... import defaults
from .data import Data

class Colorplot(Data):

    def __init__(self, *args, **kwargs):
        Data.__init__(self, **kwargs)
        defaults.kwargs(self, kwargs)
        self.process_args(args)

    def process_args(self, args):
        if len(args) == 3:
            self.x, self.y, self.z_mesh = args
        elif len(args) == 1:
            self.z_mesh = args[0]
        else:
            self.incorrect_positional_args_exception(args)

    def incorrect_positional_args_exception(self, args):
        message = (f"Colorplot takes 1 or 3 positional arguments, got {len(args)}\n"
                   "If one given, it is assumed to be the mesh data\n"
                   "If three are given, it is expected to be in the form (x, y, z)")
        raise Exception(message)

defaults.load(Colorplot)
