import sys

NO_DEFAULT = object()

def get_path_to_module(module_name):
    if isinstance(module_name, str):
        mod = sys.modules[module_name]
    else:
        mod = module_name

    return mod.__file__
