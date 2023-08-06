import enum
from unittest import TestCase

import typing

from uglyduck.inspector import TypeInspector
from uglyduck.parse import str_to_type


class TestEnum(enum.Enum):
    FOO = 0
    BAR = 1
    BAZ = 2


class Test:
    bool_with_type: bool = True
    bool_without_type = False
    int_with_type: int = 1
    int_without_type = 2
    str_with_type: str = 'a'
    str_without_type = 'b'

    def __init__(self, a: int, b: 'Test', c=TestEnum.BAR, *args: [str], **kwargs: dict):
        self.a = a
        self.b = b
        self.c = c


class TestInspect(TestCase):
    def setUp(self) -> None:
        TypeInspector.make_package_types_file('uglyduck', modules=['tests'])

    def test_types(self):
        TypeInspector.make_package_types_file('uglyduck', modules=['tests'])
        from uglyduck import types

        annotations = types.ITest.__annotations__
        self.assertEqual(
            annotations['bool_with_type'],
            bool
        )
        self.assertEqual(
            annotations['bool_without_type'],
            bool
        )
        self.assertEqual(
            annotations['int_with_type'],
            int
        )
        self.assertEqual(
            annotations['int_without_type'],
            int
        )
        self.assertEqual(
            annotations['str_with_type'],
            str
        )
        self.assertEqual(
            annotations['str_without_type'],
            str
        )
        self.assertEqual(
            annotations['a'],
            int
        )
        self.assertEqual(
            annotations['b'],
            'ITest'
        )


class TestParse(TestCase):
    def test_list_literal(self):
        self.assertEqual(
            str_to_type('[int]', globals()),
            typing.List[int]
        )
        self.assertEqual(
            str_to_type('[str]', globals()),
            typing.List[str]
        )
        self.assertEqual(
            str_to_type('[Test]', globals()),
            typing.List[Test]
        )

    def test_tuple_literal(self):
        self.assertEqual(
            str_to_type('(int, str)', globals()),
            typing.Tuple[int, str]
        )
        self.assertEqual(
            str_to_type('(int, str, Test)', globals()),
            typing.Tuple[int, str, Test]
        )
