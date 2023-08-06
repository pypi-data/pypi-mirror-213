import os

from matplotlib.pyplot import savefig

def save_figure(plot_obj):
    path = get_figure_path(plot_obj)
    plots_obj = plot_obj.plots_obj
    save_fig(path, plots_obj)
    plt.close()

def get_figure_path(plot_obj):
    file_name = get_file_name(plot_obj)
    file_name = f"{file_name}.{plot_obj.plots_obj.format}"
    path = os.path.join(plot_obj.plots_obj.path, file_name)
    return path

def get_file_name(plot_obj):
    if len(plot_obj.plots_obj.lines_object_groups) == 1:
        return get_base_file_name(plot_obj.plots_obj)
    else:
        return get_numbered_file_name(plot_obj)

def get_base_file_name(plot_objs):
    if plot_objs.title is None:
        return "Figure"
    else:
        return str(plot_objs.title)

def get_numbered_file_name(plot_obj):
    file_name = get_base_file_name(plot_obj.plot_objs)
    file_name = f"{file_name} {plot_obj.plot_index + 1}"
    return file_name

def save_fig(path, plots_obj):
    savefig(path,
            dpi=plots_obj.dpi,
            format=plots_obj.format,
            metadata=plots_obj.metadata,
            bbox_inches=plots_obj.bbox_inches,
            pad_inches=plots_obj.pad_inches,
            facecolor=plots_obj.facecolor,
            edgecolor=plots_obj.edgecolor,
            backend=plots_obj.backend)
