from ... import defaults

class Line():

    def __init__(self, x_values, y_values, **kwargs):
        defaults.kwargs(self, **kwargs)
        self.x_values = x_values
        self.y_values = y_values

defaults.load(Line)
