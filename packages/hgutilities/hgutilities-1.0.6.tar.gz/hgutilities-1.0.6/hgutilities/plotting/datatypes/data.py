from ... import defaults

class Data():

    def __init__(self, **kwargs):
        defaults.kwargs(self, kwargs)

    def get_frame_count(self):
        raise Exception("This data type does not have animation implemented")

defaults.load(Data)
