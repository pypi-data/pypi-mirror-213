import os
import json

def make_file(file_path):
    if not os.path.exists(file_path):
        folder_path = os.path.split(file_path)[0]
        make_folder(folder_path)
        make_empty_file(file_path)

def make_empty_file(file_path):
    with open(file_path, "w") as file:
        pass

def make_folder(folder_path):
    if not os.path.exists(folder_path):
        parent_folder_path = os.path.split(folder_path)[0]
        make_folder(parent_folder_path)
        os.mkdir(folder_path)

def make_folder_path(path):
    if os.path.isfile(path):
        path = os.path.split(path)[0]
    make_file(path)

def load_json(path, ignore_empty_or_none=True):
    if ignore_empty_or_none:
        if not os.path.exists(path) or os.stat(path).st_size == 0:
            return {}
    return do_load_json(path)

def do_load_json(path):
    with open(path, "r") as file:
        file_contents = json.load(file)
    return file_contents
