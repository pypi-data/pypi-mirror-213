# Plotting

## Contents

1. [Overview and Structure](#overview-and-structure)
    1. [Figures](#figures)
    1. [Animate](#animate)
    1. [Figure](#figure)
    1. [Plot](#plot)
    1. [Data](#data)
1. [Usage](#usage)
1. [Features](#features)
    1. [Universal Legend](#universal-legend)
    1. [Subplot Adjustment](#subplot-adjustment)

## Overview and Structure

This is a tool designed to make creating figures with multiple subplots easier. The data is prescribed, and the creation of the figures is handled by the package.

### Figures

At the top level there is a Figures object. This contains all the information about the figures to be produced. This includes the data to be plotted, the title of the figures, if the figures are going to be shown or saved, the base path to be saved to if needed, the number of subplots per figure, and any appearance settings of the plots. It organises the creation of Figure objects, as if there is too much data for one figure, it will need to be spread over multiple.

### Animate

This is a subclass of Figures, and allows the user to make animations. Creating animations is done through exactly the same process as creating figures, with one difference. The independent variables can't be animated, but the dependent variables will need to be passed in as a list or array where each element of the list or array gives the values of the variable for each frame. See the [usage](#usage) section for more details.

### Figure

The next level down is the Figure object. This arranges how the subplots will be arranged on the figure and organises the creation of the subplots, which are subsequently handled by Plot objects. Adding the title and universal legend happens here. An aspect ratio can be specified, and it will try to arrange the plots in that ratio as closely as it can.

### Plot

A Plot object is responsible for each individual subplot. The subplot title, axis labels, plot legends, and the data to be put on the subplot are handled at this level. There are subclasses of Plot for different types of data object, and these classes follow the naming convention of appending "Plot" to the name of the data object they are associated with.

### Data

This class handles the data to be plotted. The most basic is a Lines object which handles quantititive data on a 2D plot. There is also a Bars object which handles bar charts, and a Pie object that handles pie charts. Colorplot and Surface are also subclasses which work with 3 dimensional data. As a rule of thumb, if two matplotlib plotting functions are sufficiently different, their data will be handled by two distinct subclasses of Data. Here are the subclasses of Data currently implemented.

- Lines. This takes in a collection of Line objects. It also has an optional keyword argument called `plot_type` which controls whether the plot is made using `plot`, `semilogy`, `semilogx`, `loglog`, or `errorbar`. Each Line object corresponds to a single line on a subplot, and has a list of $x$ values and $y$ values. The Line object also has optional attributes that control the appearance of the line and the line label.
- Bars. This is similar to Lines, but it handles Bar objects which are similar to Line objects. The key distinction here is that the $x$ axis has qualitative data, and that prescribing the appearance of the bars is very different from lines. We note that a Bar object handles an entire series of data, and a Bars object handles a bar chart plot, so a single plot with two data series on it will be handled by one Bars object and two Bar objects.
- Pie. Pie charts cannot show multiple data series so this subclass does not have a correspondence to Line or Bar. This takes in all the arguments that the matplotlib `pie` function takes in, and also any of the arguments from the parent class, Plot.
- Colormesh. This shows a single data series with two dimensional input and one dimensional output. It takes in almost all of the arguments that the matplotlib pcolormesh function takes in and uses pcolormesh instead of pcolor.
- Surface. This shows a single data series with a two dimensional input and a one dimensional output. Different from Colormesh, this produces a plot in three spatial dimensions represented as a surface. Wireframe and 3D contour plotting is also supported by passing in "plot_wireframe" or "contour" as a value of the `plot_type` keyword

### Usage

The first step in creating a figure is specifying the data. Here is an example with plotting a single line on a graph. `lines_obj` is the Data object in this case, and we pass it in to `create_figures`.
    
    # Importing
    import numpy as np
    from hgutilities import plotting

    # Creation of Line object
    x_values = np.arange(0, 2*np.pi, 0.1)
    y_values = np.sin(x_values)
    line_obj = plotting.line(x_values, y_values)

    # Creation of Lines object
    lines_obj = plotting.lines(line_obj)

    # Creation of figures
    plotting.create_figures(lines_obj)

If we want to create multiple lines, we can pass in a list of line objects. We can also give our figure some labels.


    # Importing
    import numpy as np
    from hgutilities import plotting

    # Creation of Line object
    def get_line_obj(n):
        y_values = np.sin(n*x_values)
        label = f"n = {n}"
        line_obj = plotting.line(x_values, y_values, label=label)
        return line_obj

    x_values = np.arange(0, 2*np.pi, 0.01)
    x_coefficients = [1, 2, 3]
    line_objects = [get_line_obj(n) for n in x_coefficients]

    # Creation of Lines object
    title = "Sin(nx)"
    x_label = "My x axis label"
    y_label = "My y axis label"
    lines_obj = plotting.lines(line_objects, title=title, legend=True,
                                  x_label=x_label, y_label=y_label)

    # Creation of figures
    plotting.create_figures(lines_obj)

We could have data split across multiple subplots. By default we have `subplots=None` and all subplots will be put on a figure. If subplots is specified and the subplots do not fit on one figure, they will be distributed across multiple. The subplots will be evenly distributed over $\left \lfloor \frac{\text{total subplots}}{\text{subplots per figure}} \right \rfloor$ figures, so the number of subplots per figure is at least as big as the number specified. In future versions this behaviour will change, and the number given by the subplots keyword will be an upper bound on how many subplots there will be on a given figure, and the number of figures will be as small as possible given that constraint.

    # Importing
    import numpy as np
    from hgutilities import plotting

    def get_lines_obj(n):
        line_obj = get_line_obj(n)
        title = f"Sin({n}x)"
        x_label = "My x axis label"
        y_label = "My y axis label"
        lines_obj = plotting.lines(line_obj, title=title,
        x_label=x_label, y_label=y_label)
        return lines_obj

    def get_line_obj(n):
        y_values = np.sin(n*x_values)
        line_obj = plotting.line(x_values, y_values)
        return line_obj

    # Creation of lines objects
    x_values = np.arange(0, 2*np.pi, 0.01)
    x_coefficients = list(range(1, 13))
    lines_objects = [get_lines_obj(n) for n in x_coefficients]

    # Creation of figures
    plotting.create_figures(lines_objects, subplots=6)

You can mix the types of plot within a figure. Here is an example that shows the other types of plot supported.

    # Importing
    import numpy as np
    from hgutilities import plotting

    # Creating bars object
    x_values_1 = ["Red", "Green", "Blue"]
    y_values_1 = [4, 2, 7]
    bar_obj_1 = plotting.bar(x_values_1, y_values_1)

    x_values_2 = ["Green", "Red", "Blue"]
    y_values_2 = [1, 4, 5]
    bar_obj_2 = plotting.bar(x_values_2, y_values_2)

    title = "Bar Chart Example"
    bar_objects = [bar_obj_1, bar_obj_2]
    bars_obj = plotting.bars(bar_objects, title=title)

    # Creating pie object
    values = [4, 2, 7]
    labels = ["Red", "Green", "Blue"]
    title = "Pie Chart Example"
    pie_obj = plotting.pie(values, labels, title=title,
                           colors=labels, test=False)

    # Creating surface object
    x_values = np.arange(0, 10, 0.01)
    y_values = np.arange(0, 10, 0.01)
    x_mesh, y_mesh = np.meshgrid(x_values, y_values)
    z_mesh = np.cos(x_mesh) + np.cos(y_mesh)
    title = "Surface Plot Example"
    surface_obj = plotting.surface(x_mesh, y_mesh, z_mesh,
                                   title=title)

    # Creating colorplot object
    title = "Colorplot Example"
    colormap_obj = plotting.colorplot(x_mesh, y_mesh, z_mesh,
                                      title=title)

    # Creation of figures
    data_objects = [bars_obj, pie_obj, surface_obj, colormap_obj]
    plotting.create_figures(data_objects)

Animations can also be made by adding a dimension to the dependent variable. Currently this is only implemented for Surface objects. We note that all matplotlib figure objects need to be kept open while making the animation, so this is only suitable for short animations.

    # Importing
    import numpy as np
    from hgutilities import plotting

    # Set independent variable values
    x_values = np.arange(0, 10, 0.5)
    y_values = np.arange(0, 10, 0.5)
    x_mesh, y_mesh = np.meshgrid(x_values, y_values)

    # Set dependent variable values
    def get_z_mesh_layer(time_value):
        time_mesh = np.ones(x_mesh.shape) * time_value
        z_mesh_layer = (np.sin(x_mesh + time_mesh)
                        + np.sin(y_mesh + time_mesh))
        return z_mesh_layer

    time_values = np.arange(0, 2*np.pi, 0.5)
    z_meshes = [get_z_mesh_layer(time_value)
                for time_value in time_values]
    z_meshes = np.stack(z_meshes)

    # Creating animation
    surface_obj = plotting.surface(x_mesh, y_mesh, z_meshes)
    surface_objects = [surface_obj]
    plotting.create_animations(surface_objects)

## Features

### Universal Legend

The universal legend is a tool that can be used if all subplots in a figure have the same legend. An extra blank subplot is created and the space is used to show a legend that corresponds to all plots. This can be activated by passing `universal_legend=True` as a keyword-value pair into the `create_figures` function, and any individual legends will be overruled. Exception handling not implemented, will crash or get unexpected results if not used properly.

### Subplot Adjustment

Note: this feature has not been implemented yet. If the optional keyword argument, `adjust_subplots=True` is passed in to `create_figures` (or `create_animation`), then the matplotlib subplot adjustment tool will appear when the figures are created. The subplots are usually plotted with using the constrained layout, but in this case that will be turned off and tight layout used instead.