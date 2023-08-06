import numpy as np
from matplotlib.colors import hsv_to_rgb

from ... import defaults
from .data import Data
from .line import Line

class Lines(Data):

    def __init__(self, line_objects, **kwargs):
        Data.__init__(self, **kwargs)
        defaults.kwargs(self, kwargs)
        self.set_line_objects(line_objects)
        self.count = len(self.line_objects)

    def set_line_objects(self, line_objects):
        if isinstance(line_objects, Line):
            self.line_objects = [line_objects]
        else:
            self.set_line_objects_multiple(line_objects)

    def set_line_objects_multiple(self, line_objects):
        if np.all([isinstance(line_obj, Line)
                   for line_obj in line_objects]):
            self.line_objects = list(line_objects)
        else:
            self.bad_data_objects_exception()

    def bad_data_objects_exception(self):
        message = ("When creating a lines object you must pass "
                   "in an instance of Line or an iterable of "
                   "instances of Line")
        raise TypeError(message)

    def set_rainbow_lines(self, saturation=1, value=1):
        self.set_colours(saturation, value)
        for line_obj, colour in zip(self.line_objects, self.colours):
            line_obj.colour = colour

    def set_colours(self, saturation, value):
        hues = np.linspace(0, 1, self.count + 1)[:self.count]
        saturations = np.ones(self.count)*saturation
        values = np.ones(self.count)*value
        hsv_tuples = np.array(list(zip(hues, saturations, values)))
        self.colours = hsv_to_rgb(hsv_tuples)

defaults.load(Lines)
