import matplotlib.pyplot as plt
import numpy as np

from ... import defaults
from ..plottypes.plot import Plot

class PlotBars(Plot):

    def __init__(self, figure_obj, ax, bars_obj, **kwargs):
        Plot.__init__(self, figure_obj, ax, bars_obj, **kwargs)
        self.bars_obj = bars_obj
        self.initialise_from_bars_obj()
        defaults.kwargs(self, kwargs)

    def initialise_from_bars_obj(self):
        self.bar_objects = self.bars_obj.bar_objects
        self.between_group_spacing = self.bars_obj.between_group_spacing
        self.within_group_spacing = self.bars_obj.within_group_spacing

    def plot_data(self):
        self.preprocess_bars()
        for index, bar_obj in enumerate(self.bars_obj.bar_objects):
            self.plot_bar_obj(index, bar_obj)

    def preprocess_bars(self):
        self.group_width = 1 - self.between_group_spacing
        self.set_bar_proportions()
        self.x_offset = (self.between_group_spacing + self.bar_width - 1) / 2
        self.set_x_axis_dictionary()
        
    def set_bar_proportions(self):
        if len(self.bar_objects) == 1:
            self.set_bar_proportions_single()
        else:
            self.set_proportions_multiple()

    def set_bar_proportions_single(self):
        self.bar_width = self.group_width
        self.bar_space = self.group_width

    def set_proportions_multiple(self):
        n = len(self.bar_objects)
        self.bar_width = self.group_width / (n + (n-1) * self.within_group_spacing)
        self.bar_space = (self.group_width - n * self.bar_width) / (n - 1)

    def set_x_axis_dictionary(self):
        self.x_axis_dictionary = {}
        for bar_obj in self.bar_objects:
            for x_value in bar_obj.x_values:
                self.add_to_x_axis_dictionary(x_value)

    def add_to_x_axis_dictionary(self, x_value):
        if x_value not in self.x_axis_dictionary:
            new_dict_entry = {x_value: len(self.x_axis_dictionary)}
            self.x_axis_dictionary.update(new_dict_entry)

    def get_x_values(self, index, bar_obj):
        x_values = np.array([self.x_axis_dictionary[x_value]
                             for x_value in bar_obj.x_values])
        x_values = x_values + self.x_offset + (self.bar_width + self.bar_space) * index
        return x_values

    def plot_bar_obj(self, index, bar_obj):
        bars_obj = self.bars_obj
        x_values = self.get_x_values(index, bar_obj)
        self.ax.bar(x_values,
                    bar_obj.y_values,
                    width=self.bar_width,
                    bottom=bars_obj.bottom,
                    color=bar_obj.color,
                    edgecolor=bar_obj.edgecolor,
                    linewidth=bar_obj.linewidth,
                    tick_label=bar_obj.tick_label,
                    label=bar_obj.label,
                    xerr=bar_obj.xerr,
                    yerr=bar_obj.yerr,
                    ecolor=bar_obj.ecolor,
                    capsize=bar_obj.capsize,
                    log=bars_obj.log,
                    agg_filter=bar_obj.agg_filter,
                    alpha=bar_obj.alpha,
                    angle=bar_obj.angle,
                    animated=bars_obj.animated,
                    antialiased=bar_obj.antialiased)

    def add_axis_labels(self):
        self.add_x_label()
        self.add_y_label()

defaults.load(PlotBars)
