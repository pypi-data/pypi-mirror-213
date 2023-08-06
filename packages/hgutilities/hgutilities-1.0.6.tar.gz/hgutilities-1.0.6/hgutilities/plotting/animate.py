import PIL
import io

from matplotlib.pyplot import savefig
from matplotlib.pyplot import show

from .figures import Figures
from .. import defaults

class Animate(Figures):
    
    def __init__(self, data_objects, **kwargs):
        Figures.__init__(self, data_objects, **kwargs)
        defaults.kwargs(self, kwargs)
    
    def create_animations(self, **kwargs):
        self.process_data_objects()
        self.set_figure_objects(**kwargs)
        self.prepare_animation_settings()
        self.animate_data_objects()

    def prepare_animation_settings(self):
        self.output = None
        self.set_animation_axis_limits()
        self.set_figure_animation_settings()

    def set_animation_axis_limits(self):
        for figure_obj in self.figure_objects:
            figure_obj.set_animation_axis_limits()

    def set_figure_animation_settings(self):
        for figure_obj in self.figure_objects:
            figure_obj.maximise = self.maximise
            figure_obj.figure_size = self.figure_size

    def animate_data_objects(self):
        for figure_obj in self.figure_objects:
            self.animate_figure(figure_obj)

    def animate_figure(self, figure_obj):
        frame_count = figure_obj.get_frame_count()
        self.set_all_data_values(figure_obj)
        frames = self.get_frames(figure_obj, frame_count)
        self.save_animation(frames)

    def set_all_data_values(self, figure_obj):
        figure_obj.all_data_values = [data_obj.get_data_values()
                                      for data_obj in figure_obj.data_objects]

    def get_frames(self, figure_obj, frame_count):
        frames = [self.get_frame(figure_obj, index)
                  for index in range(frame_count)]
        return frames

    def get_frame(self, figure_obj, index):
        buffer = self.get_buffer(figure_obj, index)
        image = self.get_image(buffer, figure_obj)
        return image

    def get_buffer(self, figure_obj, index):
        figure_obj.set_data_value(index)
        figure_obj.create_figure()
        buffer = io.BytesIO()
        return buffer

    def get_image(self, buffer, figure_obj):
        savefig(buffer, dpi=figure_obj.fig.dpi)
        buffer.seek(0)
        image = PIL.Image.open(buffer)
        image = image.resize(figure_obj.figure_size_pixels)
        return image

    def save_animation(self, frames):
        animation_path = f"{self.animation_name}.{self.format}"
        frames[0].save(animation_path, loop=self.loop, save_all=True,
                       append_images=frames[1:], duration=self.duration)

defaults.load(Animate)
