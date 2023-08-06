from .figures import Figures
from .animate import Animate

def create_figures(data_objects, **kwargs):
    figures_obj = Figures(data_objects, **kwargs)
    figures_obj.create_figures(**kwargs)
    return figures_obj

def create_animations(data_objects, **kwargs):    
    figures_obj = Animate(data_objects, **kwargs)
    figures_obj.create_animations(**kwargs)
    return figures_obj
