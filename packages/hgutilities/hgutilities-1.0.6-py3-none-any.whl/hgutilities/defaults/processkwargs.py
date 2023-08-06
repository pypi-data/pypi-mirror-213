import json

from ..utils.paths import load_json
from ..utils.paths import make_folder_path

class ProcessKwargs():

    def __init__(self, obj, *args, **kwargs):
        self.set_obj(obj)
        self.set_kwargs(args, kwargs)
        self.try_process_kwargs()

    def set_obj(self, obj):
        if isinstance(obj, dict):
            raise Exception("You need to pass the object instance into 'kwargs' function")
        else:
            self.obj = obj

    def set_kwargs(self, args, kwargs):
        if len(args) > 0 and isinstance(args[0], dict):
            self.kwargs = args[0]
        else:
            self.kwargs = kwargs

    def try_process_kwargs(self):
        if hasattr(self.obj, "defaults_path"):
            self.process_kwargs()

    def process_kwargs(self):
        self.key_words_to_add = []
        self.process_key_words()
        self.add_key_words_to_defaults()

    def process_key_words(self):
        for key_word, value in self.kwargs.items():
            self.process_key_word(key_word, value)

    def process_key_word(self, key_word, value):
        setattr(self.obj, key_word, value)
        if key_word not in self.obj.defaults:
            self.key_words_to_add.append(key_word)

    def add_key_words_to_defaults(self):
        if self.add_extra_defaults_to_file():
            self.do_add_key_words_to_defaults()

    def add_extra_defaults_to_file(self):
        if "add_input_kwargs_to_file" in self.obj.defaults:
            return self.obj.defaults["add_input_kwargs_to_file"]
        else:
            return False

    def do_add_key_words_to_defaults(self):
        original_file_contents = load_json(self.obj.defaults_path, ignore_empty_or_none=True)
        new_file_contents = self.add_key_words_to_file_contents(original_file_contents)
        self.save_file_contents(original_file_contents, new_file_contents)

    def add_key_words_to_file_contents(self, original_file_contents):
        new_file_contents = dict(original_file_contents)
        for key_word in self.key_words_to_add:
            if key_word not in original_file_contents:
                new_file_contents.update({key_word: None})
        return new_file_contents

    def save_file_contents(self, original_file_contents, new_file_contents):
        if len(original_file_contents) != len(new_file_contents):
            make_folder_path(self.obj.defaults_path)
            with open(self.obj.defaults_path, "w") as file:
                json.dump(new_file_contents, file, indent=2)
