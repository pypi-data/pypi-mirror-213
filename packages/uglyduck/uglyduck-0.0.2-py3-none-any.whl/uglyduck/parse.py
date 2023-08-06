import inspect
import re
import sys

import typing


def str_list_to_types(type_list, scope, cls=tuple):
    if ',' in type_list:
        return cls(str_to_type(t.strip(), scope) for t in type_list.split(','))

    return cls(str_to_type(type_list, scope), )


def str_to_type(name: str, scope):
    name = name.strip()

    # Tuple literal
    if name.startswith('('):
        return typing.Tuple[str_list_to_types(name[1:-1], scope, tuple)]

    # generics
    if '[' in name:
        bracket_open = name.find('[')
        bracket_close = name.find(']')
        if bracket_open == 0:
            cls_type = list
        else:
            cls_name = name[:bracket_open].strip()
            cls_type = str_to_type(cls_name, scope)

        generic_type = name[bracket_open+1:bracket_close].strip()
        if cls_type in [list, typing.List]:
            return typing.List[str_to_type(generic_type, scope)]
        elif cls_type in [tuple, typing.Tuple]:
            args = str_list_to_types(generic_type, scope)
            return typing.Tuple[args]
        else:
            return typing.Any

    if '.' in name:
        module, *name_parts = name.split('.')
        module = str_to_type(module, scope)
        current = module
        for _name in name_parts:
            if current is None:
                break
            current = current.__dict__.get(_name)

        return current

    builtins = scope.get('__builtins__', {})
    if name in builtins:
        return builtins[name]

    if name in scope:
        return scope[name]
    else:
        return None


def str_to_inferred_type(code, scope):
    if re.match('^\d+', code):
        return '.' in code and float or int
    elif re.match("^['\"][^'\"]+['\"]", code):
        return str
    elif re.match("^True|False", code):
        return bool

    cls_match = re.match("([\w.]+)\(", code)
    if cls_match:
        match = cls_match.groups(0)
        if match and len(match):
            _type = str_to_type(match[0], scope)
            if isinstance(_type, type):
                return _type
        return None


def get_func_obj_self_vars(cls, method=None):
    if method is None:
        method = '__init__'

    mod = sys.modules[cls.__module__]
    try:
        annotations = cls.__dict__[method].__annotations__
    except KeyError:
        annotations = {}

    code = inspect.getsource(cls.__dict__[method])
    self_vars = re.findall(r'self\.([a-zA-Z0-9_]+)\s*:?\s*([\w.,\[\]\s]+)?\s*=\s*([^\n]+)', code)
    variables = {}
    for var in self_vars:
        if var[0].startswith('_'):
            continue

        name = var[0].strip()
        if name in annotations:
            variables[name] = annotations[name]
        elif var[1]:
            variables[var[0]] = str_to_type(var[1], mod.__dict__)
        elif var[2]:
            variables[var[0]] = str_to_inferred_type(var[2], mod.__dict__)

    return variables
