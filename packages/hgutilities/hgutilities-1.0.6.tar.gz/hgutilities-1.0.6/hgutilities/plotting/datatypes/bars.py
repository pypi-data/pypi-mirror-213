import numpy as np

from ... import defaults
from .data import Data
from .bar import Bar

class Bars(Data):

    def __init__(self, bar_objects, **kwargs):
        Data.__init__(self, **kwargs)
        defaults.kwargs(self, kwargs)
        self.set_bar_objects(bar_objects)

    def set_bar_objects(self, bar_objects):
        if isinstance(bar_objects, Bar):
            self.bar_objects = [bar_objects]
        else:
            self.set_bar_objects_multiple(bar_objects)

    def set_bar_objects_multiple(self, bar_objects):
        if np.all([isinstance(bar_obj, Bar)
                   for bar_obj in bar_objects]):
            self.bar_objects = list(bar_objects)
        else:
            self.bad_data_objects_exception()

    def bad_data_objects_exception(self):
        message = ("When creating a bars object you must pass "
                   "in an instance of bar or an iterable of "
                   "instances of bar")
        raise TypeError(message)

defaults.load(Bars)
