import numpy as np

from ... import defaults
from .data import Data

class Pie(Data):

    def __init__(self, values, labels, **kwargs):
        Data.__init__(self, **kwargs)
        defaults.kwargs(self, kwargs)
        self.set_data(values, labels)

    def set_data(self, values, labels):
        self.values = values
        self.labels = labels

defaults.load(Pie)
