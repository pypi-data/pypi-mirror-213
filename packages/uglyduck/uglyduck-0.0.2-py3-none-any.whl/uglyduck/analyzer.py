
def get_mro_names(cls):
    return [f'{t.__module__}.{t.__name__}' for t in cls.mro()]


def get_type_module(_type):
    return hasattr(_type, '__module__') and _type.__module__ or None
