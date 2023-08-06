import matplotlib.pyplot as plt
import numpy as np

from ... import defaults
from ..plottypes.plot import Plot

class PlotLines(Plot):

    @classmethod
    def set_function_dict(cls):
        cls.function_dict = {"plot": cls.plot_regular,
                             "semilogx": cls.plot_regular,
                             "semilogy": cls.plot_regular,
                             "loglog": cls.plot_regular,
                             "errorbar": cls.plot_errorbars,
                             "scatter": cls.plot_scatter}

    def __init__(self, figure_obj, ax, lines_obj, **kwargs):
        Plot.__init__(self, figure_obj, ax, lines_obj, **kwargs)
        self.lines_obj = lines_obj
        defaults.kwargs(self, kwargs)

    def plot_data(self):
        plot_type_function = self.get_plot_type_function()
        plot_function = getattr(self.ax, self.lines_obj.plot_type)
        for line_obj in self.lines_obj.line_objects:
            plot_type_function(self, plot_function, line_obj)

    def get_plot_type_function(self):
        plot_type = self.lines_obj.plot_type
        plot_type_function = self.function_dict[plot_type]
        return plot_type_function

    def plot_regular(self, plot_function, line_obj):
        plot_function(line_obj.x_values,
                      line_obj.y_values,
                      agg_filter=line_obj.agg_filter,
                      alpha=line_obj.alpha,
                      animated=self.lines_obj.animated,
                      antialiased=line_obj.antialiased,
                      clip_box=self.lines_obj.clip_box,
                      clip_on=self.lines_obj.clip_on,
                      clip_path=self.lines_obj.clip_path,
                      color=line_obj.color,
                      dash_capstyle=line_obj.dash_capstyle,
                      dash_joinstyle=line_obj.dash_joinstyle,
                      drawstyle=line_obj.drawstyle,
                      dashes=tuple(line_obj.dashes),
                      fillstyle=line_obj.fillstyle,
                      gapcolor=line_obj.gapcolor,
                      gid=line_obj.gid,
                      in_layout=line_obj.in_layout,
                      label=line_obj.label,
                      linestyle=line_obj.linestyle,
                      linewidth=line_obj.linewidth,
                      marker=line_obj.marker,
                      markeredgecolor=line_obj.markeredgecolor,
                      markeredgewidth=line_obj.markeredgewidth,
                      markerfacecolor=line_obj.markerfacecolor,
                      markerfacecoloralt=line_obj.markerfacecoloralt,
                      markersize=line_obj.markersize,
                      markevery=line_obj.markevery,
                      mouseover=line_obj.mouseover,
                      path_effects=line_obj.path_effects,
                      rasterized=line_obj.rasterized,
                      sketch_params=line_obj.sketch_params,
                      snap=line_obj.snap,
                      solid_capstyle=line_obj.solid_capstyle,
                      solid_joinstyle=line_obj.solid_joinstyle,
                      url=line_obj.url,
                      visible=line_obj.visible,
                      zorder=line_obj.zorder)

    def plot_errorbars(self, plot_function):
        plot_function(line_obj.x_values,
                      line_obj.y_values,
                      yerr=line_obj.yerr,
                      x_err=line_obj.x_err,
                      ecolor=line_obj.ecolor,
                      elinewidth=line_obj.elinewidth,
                      capsize=line_obj.capsize,
                      barsabove=line_obj.barsabove,
                      lolims=line_obj.lolims,
                      uplims=line_obj.uplims,
                      xlolims=line_obj.xlolims,
                      xuplims=line_obj.xuplims,
                      errorevery=line_obj.errorevery,
                      capthick=line_obj.capthick,
                      agg_filter=line_obj.agg_filter,
                      alpha=line_obj.alpha,
                      animated=self.lines_obj.animated,
                      antialiased=line_obj.antialiased,
                      clip_box=self.lines_obj.clip_box,
                      clip_on=self.lines_obj.clip_on,
                      clip_path=self.lines_obj.clip_path,
                      color=line_obj.color,
                      dash_capstyle=line_obj.dash_capstyle,
                      dash_joinstyle=line_obj.dash_joinstyle,
                      dashes=tuple(line_obj.dashes),
                      drawstyle=line_obj.drawstyle,
                      fillstyle=line_obj.fillstyle,
                      gapcolor=line_obj.gapcolor,
                      gid=line_obj.gid,
                      in_layout=line_obj.in_layout,
                      label=line_obj.label,
                      linestyle=line_obj.linestyle,
                      linewidth=line_obj.linewidth,
                      marker=line_obj.marker,
                      markeredgecolor=line_obj.markeredgecolor,
                      markeredgewidth=line_obj.markeredgewidth,
                      markerfacecolor=line_obj.markerfacecolor,
                      markerfacecoloralt=line_obj.markerfacecoloralt,
                      markersize=line_obj.markersize,
                      markevery=line_obj.markevery,
                      mouseover=line_obj.mouseover,
                      path_effects=line_obj.path_effects,
                      rasterized=line_obj.rasterized,
                      sketch_params=line_obj.sketch_params,
                      snap=line_obj.snap,
                      solid_capstyle=line_obj.solid_capstyle,
                      solid_joinstyle=line_obj.solid_joinstyle,
                      transform=line_obj.transform,
                      url=line_obj.url,
                      visible=line_obj.visible,
                      zorder=line_obj.zorder)

    def plot_scatter(self, plot_function):
        plot_function(line_obj.x_values,
                      line_obj.y_values,
                      s=line_obj.markersize,
                      c=line_obj.color,
                      marker=line_obj.marker,
                      cmap=line_obj.cmap,
                      norm=line_obj.norm,
                      vmin=line_obj.vmin,
                      vmax=line_obj.vmax,
                      alpha=line_obj.alpha,
                      linewidths=line_obj.linewidths,
                      edgecolors=line_obj.edgecolors,
                      plotnonfinite=line_obj.plotnonfinite)

    def add_axis_labels(self):
        self.add_x_label()
        self.add_y_label()

defaults.load(PlotLines)
