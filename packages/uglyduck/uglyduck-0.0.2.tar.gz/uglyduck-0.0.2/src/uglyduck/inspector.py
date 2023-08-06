import enum
import importlib
import inspect
import sys
import types

import typing
from collections import OrderedDict

from uglyduck import parse, utils, analyzer

NO_DEFAULT = utils.NO_DEFAULT

CLASS_MAP = {}
INSPECTOR_CLASS_MAP = {}


def build_cls_path(cls):
    return f'{cls.__module__}.{cls.__name__}'


def add_class_map(cls):
    CLASS_MAP[build_cls_path(cls)] = cls


def add_inspector_class_map(inspector_cls):
    add_class_map(inspector_cls.cls)
    INSPECTOR_CLASS_MAP[build_cls_path(inspector_cls.cls)] = inspector_cls


def is_class_inspected(cls):
    return build_cls_path(cls) in INSPECTOR_CLASS_MAP


def get_class_map(cls):
    return CLASS_MAP.get(build_cls_path(cls))


def get_inspector_class_from_cls(cls) -> 'TypeInspectorClass':
    return INSPECTOR_CLASS_MAP.get(build_cls_path(cls))


def is_class_mapped(cls) -> bool:
    return build_cls_path(cls) in CLASS_MAP


class ParameterKind(enum.Enum):
    POSITIONAL = 0
    ARGS = 1
    KWARGS = 2


class TypeInspectorFunctionParameter:
    def __init__(self, name, typehint=None, default=None, kind=ParameterKind.POSITIONAL):
        self.name = name
        self.typehint = typehint
        self.default = default
        self.kind = kind

    def __str__(self):
        unpack = ''
        if self.kind == ParameterKind.ARGS:
            unpack = '*'
        elif self.kind == ParameterKind.KWARGS:
            unpack = '**'

        typehint = self.typehint and f': {self.typehint}' or ''
        default = self.default and f' = {self.default}' or ''
        return f'{unpack}{self.name}{typehint}{default}'


class TypeInspectorFunction:
    def __init__(self, name, parameters: [TypeInspectorFunctionParameter] = None, return_type=None, indent=4):
        if parameters is None:
            parameters = []

        self.name = name
        self.parameters = parameters
        self.return_type = return_type
        self.indent = indent

    def __str__(self):
        return_type = self.return_type and f' -> {self.return_type}' or ''
        parameters = self.parameters and ', '.join([str(p) for p in self.parameters]) or ''
        return f"""
{' ' * self.indent}def {self.name}({parameters}){return_type}:
{' ' * self.indent}    ...
"""

    @classmethod
    def get_stuff(cls, inspector: 'TypeInspector', method):
        arguments = []
        annotations = method.__annotations__
        method_signature = inspect.signature(method)

        for name in method_signature.parameters.keys():
            default = method_signature.parameters[name].default
            param_kind = ParameterKind.POSITIONAL
            if name in method_signature.parameters:
                if method_signature.parameters[name].kind == inspect.Parameter.VAR_KEYWORD:
                    param_kind = ParameterKind.KWARGS
                elif method_signature.parameters[name].kind == inspect.Parameter.VAR_POSITIONAL:
                    param_kind = ParameterKind.ARGS

            if str(default) == "<class 'inspect._empty'>":
                default = NO_DEFAULT

            if name == 'self':
                arguments.append(TypeInspectorFunctionParameter(name, kind=param_kind))
            elif name in annotations:
                param = annotations[name]
                type_name, default = inspector.get_type_name_and_default(param, default)
                arguments.append(TypeInspectorFunctionParameter(name, type_name, default, param_kind))
            elif default != NO_DEFAULT:
                param = method_signature.parameters[name].default
                type_name, default = inspector.get_type_name_and_default(param, default)
                arguments.append(TypeInspectorFunctionParameter(name, type_name, default, param_kind))
            else:
                default = inspector.get_default(default)
                arguments.append(TypeInspectorFunctionParameter(name, default=default, kind=param_kind))

        if 'return' in annotations:
            return_type = annotations['return']
            return_annotation = inspector.get_type_name(return_type)
        else:
            return_annotation = ''

        return arguments, return_annotation


    @classmethod
    def from_function(cls, inspector, function, indent=4):
        params, return_annotation = cls.get_stuff(inspector, function)
        return cls(function.__name__, params, return_annotation, indent)

    @classmethod
    def from_method(cls, inspector, method, inspector_cls, indent=4):
        params, return_annotation = cls.get_stuff(inspector, method)
        return cls(method.__name__, params, return_annotation, indent)


class TypeInspectorClassAttribute:
    def __init__(self, inspector, name, return_type=None, indent=4):
        self.inspector = inspector
        self.name = name
        self.return_type = return_type

    def __str__(self):
        return f"{self.name}: {self.inspector.get_type_name(self.return_type)}"

    @classmethod
    def from_property(cls, inspector, name: str, method_signature):
        return_type = method_signature.return_annotation
        return cls(inspector, name, return_type)


class TypeInspectorClass:
    def __init__(self, inspector, cls):
        self.inspector = inspector
        self.cls = cls
        self.name = cls.__name__
        self.protocol_name = f'I{self.name}'
        self.parents = []
        self.attributes = {}
        self.methods = {}
        self.class_methods = {}
        self.static_methods = {}
        self.init_attributes = {}

        try:
            self.annotations = cls.__annotations__
        except AttributeError:
            self.annotations = {}

        self.find_parents()
        self.process_members()

    def __str__(self):
        parent_classes = ', '.join(reversed(self.parents))
        code = f"""\n
class {self.protocol_name}({parent_classes}):
"""

        code += '\n'.join([f"    {attr}" for attr in self.attributes.values()])

        if self.init_attributes:
            code += '\n    # __init__ attributes\n'
            for name, _type in self.init_attributes.items():
                if name in self.attributes:
                    continue

                return_name = self.inspector.get_type_name(_type)
                code += f'    {name}: {return_name}\n'

        for method in self.methods.values():
            code += str(method)

        for method in self.class_methods.values():
            code += f'\n    @classmethod{method}'

        for method in self.static_methods.values():
            code += f'\n    @staticmethod{method}'

        if len(self.attributes) == 0 and len(self.methods) == 0 and len(self.class_methods) == 0 and len(self.init_attributes) == 0:
            code += '    pass\n'

        return code

    def find_parents(self):
        typing_protocol = 'typing.Protocol'
        self.parents = [typing_protocol]
        all_parents = []

        for parent_cls in self.cls.mro():
            if parent_cls == self.cls:
                continue

            if is_class_mapped(parent_cls):
                if typing_protocol in self.parents:
                    self.parents.remove(typing_protocol)

                cls_inspector = get_inspector_class_from_cls(parent_cls)
                proto = cls_inspector.protocol_name
                all_parents.extend(cls_inspector.parents)

                if not proto in all_parents:
                    self.parents.insert(0, proto)

                    if is_class_mapped(parent_cls) and not parent_cls.__module__ in self.inspector.modules:
                        parent_cls_inspector = get_inspector_class_from_cls(parent_cls)
                        self.inspector.add_import(
                            parent_cls_inspector.inspector.types_module,
                            parent_cls_inspector.protocol_name
                        )

        if '__iter__' in self.cls.__dict__:
            iter_annotations = self.cls.__dict__['__iter__'].__annotations__
            if 'return' in iter_annotations:
                iter_type = 'typing.Any'
                if isinstance(iter_annotations['return'], typing._GenericAlias):
                    iter_type = iter_annotations['return'].__args__[0]
                    if isinstance(iter_type, typing.ForwardRef):
                        iter_type = self.inspector.get_type_name(iter_type.__forward_arg__)
                    else:
                        iter_type = self.inspector.get_type_name(iter_type)

                self.parents.append(f"typing.Iterable[{iter_type}]")

    def process_members(self):
        for name, method in self.cls.__dict__.items():
            if name.startswith('_') and name != '__init__':
                continue

            if isinstance(method, type):
                pass
            elif isinstance(method, types.FunctionType):
                self.methods[name] = TypeInspectorFunction.from_method(self.inspector, method, self)
            elif isinstance(method, classmethod):
                self.class_methods[name] = TypeInspectorFunction.from_method(self.inspector, method.__func__, self)
            elif isinstance(method, staticmethod):
                self.static_methods[name] = TypeInspectorFunction.from_method(self.inspector, method.__func__, self)
            elif isinstance(method, property):
                self.attributes[name] = TypeInspectorClassAttribute.from_property(
                    self.inspector,
                    name,
                    inspect.signature(method.fget)
                )
            else:
                if name in self.annotations:
                    self.attributes[name] = TypeInspectorClassAttribute(
                        self.inspector,
                        name,
                        self.annotations[name]
                    )
                else:
                    self.attributes[name] = TypeInspectorClassAttribute(
                        self.inspector,
                        name,
                        method
                    )

        if '__init__' in self.cls.__dict__:
            self.init_attributes = parse.get_func_obj_self_vars(self.cls)


class TypeInspector:
    def __init__(self, package, module_path, modules=None, ignore=None):
        self.package = package
        self.module_path = module_path
        self.imports = ['typing']
        self.functions = {}
        self.classes: dict = {}
        self.current_module = None

        if modules is not None:
            modules_to_type = []
            for module_name in modules:
                if module_name not in sys.modules:
                    importlib.import_module(module_name)
            for sys_module_name in sys.modules:
                for module_name in modules:
                    if sys_module_name.startswith(module_name):
                        modules_to_type.append(sys_module_name)
                        break
        else:
            modules_to_type = [module for module in sys.modules if module.startswith(package)]

        self.modules = modules_to_type

        for module_name in self.modules:
            if module_name.endswith('.types') or module_name in ignore:
                continue

            try:
                mod = sys.modules[module_name]
            except KeyError:
                mod = importlib.import_module(module_name)

            module = mod.__dict__
            items = module.keys()
            self.current_module = mod

            items_to_make = []
            for item in items:
                if item.startswith('_'):
                    continue

                if not callable(module[item]) or not inspect.isclass(module[item]):
                    continue

                if module[item].__module__ != module_name:
                    continue

                self.prepare_item(module[item])
                items_to_make.append(module[item])

            for item in items_to_make:
                self.make_item(item)

    def __str__(self):
        code_items = []
        for name, cls in self.classes.items():
            code_items.append(str(cls))

        return '\n'.join(code_items)

    @property
    def types_module(self):
        return self.package + '.types'

    def is_interface_method_name(self, name):
        return len(name) > 1 and name.startswith('I') and name[1].isupper()

    def add_import(self, from_path, to_import=None):
        if from_path == 'inspect' and to_import == '_empty':
            return

        if to_import is None:
            self.imports.append(from_path)
        else:
            self.imports.append((from_path, to_import))

    def get_default(self, default):
        if default == NO_DEFAULT:
            return ''
        return str(default)

    def get_type_name_and_default(self, t, default):
        type_name = self.get_type_name(t)
        if type_name == 'str' and isinstance(default, str) and default != NO_DEFAULT:
            if not (default.startswith('"') and default.endswith('"')) and not (default.startswith("'") and default.endswith("'")):
                default = f"'{default}'"
        return type_name, self.get_default(default)

    def get_type_name(self, t):
        _type = type(t)

        if analyzer.get_type_module(_type) == 'types' and isinstance(t, types.GenericAlias):
            str_type = str(t)
            if str_type.startswith('list['):
                t = list(t.__args__)
                _type = type(t)

        if isinstance(t, type):
            if t.__module__ not in ['builtins', self.current_module.__name__]:
                self.add_import(t.__module__, t.__name__)

            if t.__module__ in self.modules:
                cls_inspector = get_inspector_class_from_cls(t)
                if cls_inspector:
                    type_name = cls_inspector.protocol_name
                else:
                    type_name = f"Fail{t.__name__}"
            else:
                if self.is_interface_method_name(t.__name__):
                    type_name = f"'{t.__name__}'"
                else:
                    type_name = t.__name__
        elif isinstance(t, types.FunctionType):
            type_name = self.get_type_name(t.__annotations__.get('return', typing.Any))
        elif isinstance(t, tuple):
            items = ', '.join([self.get_type_name(item) for item in t])
            type_name = f'typing.Tuple[{items}]'
        elif _type in [
            list,
            typing.List,
        ]:
            if len(t) == 0:
                type_name = 'typing.List[typing.Any]'
            else:
                list_type = self.get_type_name(t[0])
                type_name = f'typing.List[{list_type}]'
        elif isinstance(t, dict):
            items = ', '.join([self.get_type_name(item) for item in t])
            type_name = f'typing.Dict[{items}]'
        elif isinstance(t, (int, float, bool, str)):
            if isinstance(t, str) and str(t) in self.current_module.__dict__ or str(t) in self.classes:
                if self.is_interface_method_name(t):
                    type_name = f"'{t}'"
                else:
                    type_name = f"'I{t}'"
            else:
                type_name = type(t).__name__
        else:
            if analyzer.get_type_module(t) in ['typing', 'types']:
                if _type in [
                    types.GenericAlias,
                    typing._UnionGenericAlias,
                    typing._GenericAlias,
                ]:
                    type_cls_name = str(t).split('[')[0]
                    type_name = f'{type_cls_name}[{self.get_type_name(t.__args__[0])}]'
                elif _type == typing.ForwardRef:
                    forward_ref = t.__forward_arg__
                    if forward_ref in self.current_module.__dict__:
                        type_name = f"'I{forward_ref}'"
                    else:
                        type_name = t.__forward_arg__
                else:
                    type_name = str(t)
            else:
                cls = t.__class__
                if cls.__module__ != 'builtins':
                    self.add_import(cls.__module__, cls.__name__)
                type_name = str(cls.__name__)

        if type_name in [
            'NoneType',
            '_empty',
        ]:
            type_name = 'typing.Any'

        return type_name

    def make_class_protocol(self, cls):
        if is_class_inspected(cls):
            return get_inspector_class_from_cls(cls)

        cls_inspector = TypeInspectorClass(self, cls)
        self.classes[cls.__name__] = cls_inspector
        add_inspector_class_map(cls_inspector)

    def make_protocol_function(self, func, indent=4):
        self.functions[func.__name__] = TypeInspectorFunction.from_function(self,func, indent=indent)

    def prepare_item(self, item):
        if isinstance(item, type):
            add_class_map(item)

    def make_item(self, item):
        if isinstance(item, type):
            self.make_class_protocol(item)
        elif isinstance(item, types.FunctionType):
            self.make_protocol_function(item, indent=0)

    def make_imports(self):
        module_import = {}
        to_import = []

        for imp in self.imports:
            if isinstance(imp, str):
                to_import.append(f"import {imp}\n")
            else:
                module, name = imp
                if module in self.modules:
                    continue

                if module == self.module_path:
                    continue

                if module not in module_import:
                    module_import[module] = []
                module_import[module].append(name)

        for module, names in module_import.items():
            names = sorted(list(set(names)))
            to_import.append(f"from {module} import {', '.join(names)}\n")

        to_import = list(set(to_import))
        to_import = sorted(to_import, reverse=True)
        return ''.join(to_import)

    @classmethod
    def make_package_types_file(cls, package, modules=None, ignore=None):
        if ignore is None:
            ignore = []

        path = utils.get_path_to_module(package)
        path = '/'.join(path.split('/')[:-1])
        export_to = f'{path}/types.py'
        module_path = f'{package}.types'
        inspector = cls(package, module_path, modules, ignore)

        code_str = str(inspector)
        import_str = inspector.make_imports() # Call after str(inspector) to get all imports
        #print(f"{import_str}\n# Generated with uglyduck\n\n{code_str}")
        with open(export_to, 'w') as f:
             f.write(f"{import_str}\n# Generated with uglyduck\n\n{code_str}")
