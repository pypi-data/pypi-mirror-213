import os
import traceback
import inspect
import sys

class Docs():

    def __init__(self):
        self.extract_package()
        self.process_package_directory()
        self.add_package_docs()

    def extract_package(self):
        frame = inspect.stack()[3]
        module = inspect.getmodule(frame[0])
        self.package_path = os.path.split(module.__file__)[0]
        self.package_name = module.__name__
        self.package = sys.modules[self.package_name]

    def process_package_directory(self):
        for name, obj in inspect.getmembers(self.package):
            if not inspect.ismodule(obj):
                if hasattr(obj, "__module__"):
                    self.filter_non_module_objects(obj)

    def filter_non_module_objects(self, obj):
        object_module = inspect.getmodule(obj)
        common_path = self.get_common_path(object_module)
        if common_path == self.package_path:
            self.set_object_docs(obj)

    def get_common_path(self, object_module):
        object_module_path = object_module.__file__
        common_path = os.path.commonpath((self.package_path, object_module_path))
        return common_path

    def set_object_docs(self, obj):
        doc_path = self.get_doc_path(obj)
        doc_string = self.get_doc_string_from_path(doc_path)
        obj.__doc__ = doc_string

    def get_doc_path(self, obj):
        module = sys.modules[obj.__module__]
        folder_path = os.path.split(module.__file__)[0]
        name = os.path.splitext(obj.__name__)[0]
        doc_path = self.get_doc_path_from_path_data(folder_path, name)
        return doc_path

    def get_doc_path_from_path_data(self, folder_path, name):
        doc_file_name = f"{name}.txt"
        doc_path = os.path.join(folder_path, "Documentation", doc_file_name)
        return doc_path

    def get_doc_string_from_path(self, doc_path):
        if os.path.exists(doc_path):
            return self.get_doc_string_from_existing_path(doc_path)
        else:
            return self.get_doc_string_from_non_existing_path(doc_path)

    def get_doc_string_from_existing_path(self, doc_path):
        with open(doc_path, "r") as file:
            doc_string = "".join([line for line in file])
        return doc_string

    def get_doc_string_from_non_existing_path(self, doc_path):
        return ("No documentation exists for this object.\n"
                "It was expected to be found at the following location:\n"
                f"{doc_path}\n")

    def add_package_docs(self):
        doc_path = self.get_package_doc_path()
        doc_string = self.get_doc_string_from_path(doc_path)
        self.package.__doc__ = doc_string

    def get_package_doc_path(self):
        name = self.package.__name__.split(".")[-1]
        doc_path = self.get_doc_path_from_path_data(self.package_path, name)
        return doc_path

def docs():
    docs_obj = Docs()
