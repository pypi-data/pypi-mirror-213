import os
import __main__

import numpy as np

from .. import defaults
from .figure import Figure
from .datatypes.data import Data
from ..utils.groups import get_group_indexes
from ..utils.groups import get_group_size
from ..utils.paths import make_folder

class Figures():

    def __init__(self, data_objects, **kwargs):
        defaults.kwargs(self, **kwargs)
        self.set_data_objects(data_objects)
        self.data_obj_count = self.data_objects.size

    def set_data_objects(self, data_objects):
        if isinstance(data_objects, Data):
            self.data_objects = np.array([data_objects])
        else:
            self.set_data_objects_multiple(data_objects)

    def set_data_objects_multiple(self, data_objects):
        if np.all([isinstance(data_obj, Data)
                   for data_obj in data_objects]):
            self.data_objects = np.array(data_objects)
        else:
            self.bad_data_objects_exception()

    def bad_data_objects_exception(self):
        message = ("When creating figure objects you must pass "
                   "in an instance of Data or an iterable of "
                   "instances of Data. If you are passing in "
                   "Line/Bar objects, you need to create a "
                   "Lines/Bars object to pass in instead")
        raise TypeError(message)
    
    def create_figures(self, **kwargs):
        self.process_data_objects()
        self.process_output_mode()
        self.plot_data_objects(**kwargs)

    def process_output_mode(self):
        if self.output == "Save":
            self.create_plots_folder()

    def create_plots_folder(self):
        if self.path is None:
            self.path = os.path.split(__main__.__file__)[0]
        make_folder(self.path)

    def process_data_objects(self):
        self.subplots = get_group_size(self.subplots, self.data_objects)
        group_indexes = get_group_indexes(self.data_obj_count, self.subplots)
        self.data_object_groups = [self.data_objects[indexes]
                                    for indexes in group_indexes]

    def plot_data_objects(self, **kwargs):
        self.set_figure_objects(**kwargs)
        for figure_obj in self.figure_objects:
            figure_obj.create_figure()

    def set_figure_objects(self, **kwargs):
        data_obj_iterable = enumerate(self.data_object_groups)
        self.figure_objects = [Figure(self, data_object_group, index, **kwargs)
                               for index, data_object_group in data_obj_iterable]

defaults.load(Figures)
