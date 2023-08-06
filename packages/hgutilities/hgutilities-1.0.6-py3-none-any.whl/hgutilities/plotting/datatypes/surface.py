import numpy as np

from ... import defaults
from .data import Data

class Surface(Data):

    def __init__(self, x_values, y_values, z_values, **kwargs):
        Data.__init__(self, **kwargs)
        self.set_xyz_values(x_values, y_values, z_values)
        defaults.kwargs(self, kwargs)

    def set_xyz_values(self, x_values, y_values, z_values):
        self.x_values = x_values
        self.y_values = y_values
        self.z_values = z_values

    def set_animation_axis_limits(self):
        max_z = np.max(self.z_values)
        min_z = np.min(self.z_values)
        self.z_limits = [min_z, max_z]

    def get_frame_count(self):
        if len(self.z_values.shape) == 3:
            return self.z_values.shape[0]
        else:
            raise ValueError("z_values needs 3 dimensions to animate")

    def get_data_values(self):
        return np.copy(self.z_values)

    def set_data_value(self, data_value):
        self.z_values = data_value

defaults.load(Surface)
