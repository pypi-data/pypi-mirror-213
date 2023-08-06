import matplotlib.pyplot as plt
import matplotlib.font_manager
import numpy as np

from ... import defaults
from ...utils.dicts import remove_none_values

class Plot():

    @classmethod
    def set_function_dict(cls):
        pass
    
    def __init__(self, figure_obj, ax, data_obj, **kwargs):
        self.set_figure_obj(figure_obj)
        self.ax = ax
        self.data_obj = data_obj
        defaults.kwargs(self, kwargs)
        self.set_kwargs()

    def set_kwargs(self):
        self.inherit_kwargs()
        self.set_font_kwargs()

    def inherit_kwargs(self):
        attributes = ["title_fontname", "title_fontsize",
                      "title_color", "title_verticalalignment",
                      "title_horizontalalignment", "title_y",
                      "title_pad", "title_loc",
                      "axis_fontname", "axis_fontsize",
                      "axis_color", "axis_labelpad", "axis_loc",
                      "x_axis_rotation", "y_axis_rotation", "z_axis_rotation"]
        defaults.inherit(self.data_obj, self.figure_obj, attributes)
        
    def set_font_kwargs(self):
        self.set_title_fontdict()
        self.set_axis_fontdict()

    def set_title_fontdict(self):
        kwargs = {"fontname": self.data_obj.title_fontname,
                  "fontsize": self.data_obj.title_fontsize,
                  "color": self.data_obj.title_color,
                  "verticalalignment": self.data_obj.title_verticalalignment,
                  "horizontalalignment": self.data_obj.title_horizontalalignment}
        self.title_fontdict = remove_none_values(kwargs)

    def set_axis_fontdict(self):
        kwargs = {"fontname": self.data_obj.axis_fontname,
                  "fontsize": self.data_obj.axis_fontsize,
                  "color": self.data_obj.axis_color}
        self.axis_fontdict = remove_none_values(kwargs)

    def set_figure_obj(self, figure_obj):
        self.figure_obj = figure_obj
        self.figures_obj = figure_obj.figures_obj

    def create_plot(self):
        self.plot_data()
        self.set_title()
        self.add_legend()
        self.add_axis_labels()

    def set_title(self):
        if self.data_obj.title is not None:
            self.ax.set_title(self.data_obj.title, **self.title_fontdict,
                              loc=self.data_obj.title_loc, y=self.data_obj.title_y,
                              pad=self.data_obj.title_pad)
    
    def add_legend(self):
        if not self.figures_obj.universal_legend:
            if self.data_obj.legend:
                self.ax.legend(loc=self.data_obj.legend_loc)

    def add_axis_labels(self):
        pass

    def add_x_label(self):
        if self.data_obj.x_label is not None:
            self.ax.set_xlabel(self.data_obj.x_label,
                               **self.axis_fontdict)

    def add_y_label(self):
        if self.data_obj.y_label is not None:
            self.ax.set_ylabel(self.data_obj.y_label,
                               **self.axis_fontdict)

    def add_z_label(self):
        if self.data_obj.z_label is not None:
            self.ax.set_zlabel(self.data_obj.z_label,
                               **self.axis_fontdict)

defaults.load(Plot)
