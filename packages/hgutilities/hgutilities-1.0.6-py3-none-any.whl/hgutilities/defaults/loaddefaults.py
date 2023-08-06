import traceback
import inspect
import os
import json

from ..utils.paths import make_file
from ..utils.paths import load_json

class LoadDefaults():

    def __init__(self, cls):
        self.cls = cls
        self.set_defaults_path()
        self.set_defaults()

    def set_defaults_path(self):
        module_path = traceback.extract_stack()[-3].filename
        parent_path, module_file_name = os.path.split(module_path)
        defaults_file_name = f"{self.cls.__name__}.txt"
        self.cls.defaults_path = os.path.join(parent_path, "Default Settings", defaults_file_name)

    def set_defaults(self):
        self.cls.defaults = {}
        self.add_defaults_from_ancestors()
        self.add_defaults_from_file()
        self.set_default_values()

    def add_defaults_from_ancestors(self):
        ancestors = self.cls.__mro__[-2:0:-1]
        for ancestor in ancestors:
            self.add_defaults_from_ancestor(ancestor)

    def add_defaults_from_ancestor(self, ancestor):
        for key_word, value in ancestor.defaults.items():
            self.cls.defaults.update({key_word: value})

    def add_defaults_from_file(self):
        defaults_from_file = load_json(self.cls.defaults_path, ignore_empty_or_none=True)
        for key_word, value in defaults_from_file.items():
            self.cls.defaults.update({key_word: value})

    def set_default_values(self):
        for parameter_name, parameter_value in self.cls.defaults.items():
            setattr(self.cls, parameter_name, parameter_value)
