from ..defaults import docs

# Functions and classes to be accessed by the user
from .plotfunctions import create_figures
from .plotfunctions import create_animations
from .datatypes.line import Line as line
from .datatypes.lines import Lines as lines
from .datatypes.bars import Bars as bars
from .datatypes.bar import Bar as bar
from .datatypes.pie import Pie as pie
from .datatypes.surface import Surface as surface
from .datatypes.colorplot import Colorplot as colorplot

# Classes that need initialisation
from .figure import Figure
from .plottypes.plotlines import PlotLines
from .plottypes.plotbars import PlotBars
from .plottypes.plotpie import PlotPie
from .plottypes.plotsurface import PlotSurface
from .plottypes.plotcolorplot import PlotColorplot

# Initialising classes
Figure.set_plot_classes()
PlotLines.set_function_dict()
PlotBars.set_function_dict()
PlotPie.set_function_dict()
PlotSurface.set_function_dict()
PlotColorplot.set_function_dict()

# Importing other classes that have documentation
# files so they can be detected by defaults.doc
from .animate import Animate

docs()
