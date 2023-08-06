import matplotlib.pyplot as plt
import numpy as np

from ... import defaults
from ..plottypes.plot import Plot

class PlotSurface(Plot):

    @classmethod
    def set_function_dict(cls):
        cls.function_dict = {"plot_surface": cls.plot_surface,
                             "plot_wireframe": cls.plot_wireframe,
                             "contour": cls.plot_contour}

    def __init__(self, figure_obj, ax, data_obj, **kwargs):
        Plot.__init__(self, figure_obj, ax, data_obj, **kwargs)
        defaults.kwargs(self, kwargs)

    def plot_data(self):
        function_type = self.get_plot_function()
        plot_function = getattr(self.ax, self.data_obj.plot_type)
        function_type(self, plot_function, self.data_obj)
        self.set_z_limits()
        self.set_axes()

    def get_plot_function(self):
        plot_type = self.data_obj.plot_type
        plot_function = self.function_dict[plot_type]
        return plot_function

    def plot_surface(self, plot_function, data_obj):
        plot_function(data_obj.x_values,
                      data_obj.y_values,
                      data_obj.z_values,
                      color=data_obj.color,
                      cmap=data_obj.cmap,
                      facecolors=data_obj.facecolors,
                      norm=data_obj.norm,
                      vmin=data_obj.vmin,
                      vmax=data_obj.vmax,
                      shade=data_obj.shade,
                      lightsource=data_obj.lightsource)
    
    def plot_wireframe(self, plot_function, data_obj):
        plot_function(data_obj.x_values,
                      data_obj.y_values,
                      data_obj.z_values,
                      rcount=data_obj.rcount,
                      ccount=data_obj.ccount,
                      colors=data_obj.colors,
                      cmap=data_obj.cmap,
                      facecolors=data_obj.facecolors,
                      norm=data_obj.norm,
                      segments=data_obj.segments,
                      linewidths=data_obj.linewidths,
                      antialiased=data_obj.antialiased,
                      zorder=data_obj.zorder,
                      edgecolors=data_obj.edgecolors,
                      linestyles=data_obj.linestyles,
                      capstyle=data_obj.capstyle,
                      joinstyle=data_obj.joinstyle,
                      offsets=data_obj.offsets,
                      offset_transform=data_obj.offset_transform,
                      hatch=data_obj.hatch)

    def plot_contour(self, plot_function, data_obj):
        plot_function(data_obj.x_values,
                      data_obj.y_values,
                      data_obj.z_values,
                      extend3d=data_obj.extend3d,
                      stride=data_obj.stride,
                      zdir=data_obj.zdir,
                      offset=data_obj.offset,
                      levels=data_obj.levels,
                      corner_mask=data_obj.corner_mask,
                      colors=data_obj.colors,
                      cmap=data_obj.cmap,
                      norm=data_obj.norm,
                      vmin=data_obj.vmin,
                      vmax=data_obj.vmax,
                      origin=data_obj.origin,
                      extent=data_obj.extent,
                      locator=data_obj.locator,
                      extend=data_obj.extend)
    
    def set_z_limits(self):
        if self.data_obj.z_limits is not None:
            bottom, top = self.data_obj.z_limits
            self.ax.set_zlim(bottom=bottom, top=top)

    def set_axes(self):
        if not self.data_obj.axes:
            self.ax.axis("off")

defaults.load(PlotSurface)
