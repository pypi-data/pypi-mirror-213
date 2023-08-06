import matplotlib.pyplot as plt
import matplotlib.font_manager
import numpy as np

from ... import defaults
from ..plottypes.plot import Plot

class PlotColorplot(Plot):

    def __init__(self, figure_obj, ax, colorplot_obj, **kwargs):
        Plot.__init__(self, figure_obj, ax, colorplot_obj, **kwargs)
        self.colorplot_obj = colorplot_obj
        defaults.kwargs(self, kwargs)

    def plot_data(self):
        colorplot_obj = self.colorplot_obj
        x_and_y = self.get_x_and_y()
        self.ax.pcolormesh(*x_and_y, colorplot_obj.z_mesh,
                           cmap=colorplot_obj.cmap,
                           norm=colorplot_obj.norm,
                           vmin=colorplot_obj.vmin,
                           vmax=colorplot_obj.vmax,
                           edgecolors=colorplot_obj.edgecolors,
                           alpha=colorplot_obj.alpha,
                           shading=colorplot_obj.shading,
                           snap=colorplot_obj.snap,
                           rasterized=colorplot_obj.rasterized,
                           agg_filter=colorplot_obj.agg_filter,
                           animated=colorplot_obj.animated,
                           antialiased=colorplot_obj.antialiased,
                           capstyle=colorplot_obj.capstyle,
                           clip_box=colorplot_obj.clip_box,
                           clip_on=colorplot_obj.clip_on,
                           clip_path=colorplot_obj.clip_path,
                           color=colorplot_obj.color,
                           edgecolor=colorplot_obj.edgecolor,
                           facecolor=colorplot_obj.facecolor,
                           gid=colorplot_obj.gid,
                           hatch=colorplot_obj.hatch,
                           joinstyle=colorplot_obj.joinstyle,
                           label=colorplot_obj.label,
                           linestyle=colorplot_obj.linestyle,
                           linewidth=colorplot_obj.linewidth,
                           mouseover=colorplot_obj.mouseover,
                           offsets=colorplot_obj.offsets,
                           path_effects=colorplot_obj.path_effects,
                           visible=colorplot_obj.visible,
                           url=colorplot_obj.url,
                           zorder=colorplot_obj.zorder)

    def get_x_and_y(self):
        if ((self.colorplot_obj.x is not None) and
            (self.colorplot_obj.y is not None)):
            return (self.colorplot_obj.x, self.colorplot_obj.y)
        else:
            return ()

defaults.load(PlotColorplot)
