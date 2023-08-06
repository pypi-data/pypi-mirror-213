# Ugly Duck

Use this module to make protocols based on classes in your python project. This
project was made out of frustration with the current state of static types in
Python 3, mainly juggling with circular imports and the workaround of importing
with TYPE_CHECKING. I originally made this to generate a starting point for one
of my projects, but I ended up enjoying working with it and ended up setting it
up to work in real-time in other projects. It makes working with static typing 
in Python as easy as it is in other languages. All protocols are the class name
with an 'I' prefix. For example, a class named 'User' will have a protocol
named 'IUser'. You can then import IUser from the types.py file and use it
anywhere and not have to think about/manage imports. It's ugly, I know.

# Installation

```bash
pip install uglyduck
```

# Usage

Include the following in a package's `__init__.py` file:

```python
from uglyduck.inspector import TypeInspector

# This will create packagename/types.py with protocols for all classes in the
# models and helpers modules.
TypeInspector.make_package_types_file('packagename', modules=[
    'models',
    'helpers'
])
```

If you're using Django, you will need to run it after the app is ready in your
`apps.py` file:

```python
from django.conf import settings
from django.apps import AppConfig

from uglyduck.inspector import TypeInspector


class MyAppConfig(AppConfig):
    name = "apps.myapp"

    def ready(self):
        if settings.DEBUG:
            TypeInspector.make_package_types_file('apps.myapp', modules=[
                'models',
                'helpers'
            ])
```

# Possible Improvements

- Support inheritance from classes outside of the package.