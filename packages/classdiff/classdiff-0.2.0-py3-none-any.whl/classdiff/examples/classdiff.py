from dataclasses import dataclass

import classdiff


@dataclass
class OtherClass:
    name: str


@dataclass
class SomeResource:
    name: str
    price: float
    quantity: int
    dangerous: bool
    other: OtherClass
    not_changed: OtherClass


def main():
    added_removed_changed()
    changed_keys()
    missing_keys()
    with_dict()
    with_dataclasses()
    enum()


def added_removed_changed() -> None:
    a1 = {
        "parent": {
            "unchanged": "unchanged",
            "changed": 1,
            "changed_list": [1, 2, 3],
            "changed_dict": {
                "added": "added",
                "unchanged": "unchanged",
                "changed": "a",
            },
            "added": "added",
            "added_list": [1, 2, 3],
            "added_dict": {
                "first": 1,
            },
        }
    }
    a2 = {
        "parent": {
            "unchanged": "unchanged",
            "changed": 2,
            "changed_list": [4, 5, 6],
            "changed_dict": {
                "removed": "removed",
                "unchanged": "unchanged",
                "changed": "b",
            },
            "removed": "removed",
            "removed_list": [1, 2, 3],
            "removed_dict": {
                "second": 2,
            },
        }
    }

    for l in classdiff.diff(a1, a2):
        print(l)

    print("-" * 40)


def enum() -> None:
    from enum import Enum

    class YesOrNo(Enum):
        YES = "y"
        NO = "n"

    @dataclass
    class A:
        a: str
        v: YesOrNo

    a1 = A(a="a1", v=YesOrNo.YES)
    a2 = A(a="a2", v=YesOrNo.NO)

    for fn in [classdiff.enum_name, classdiff.enum_value, classdiff.enum_full]:
        for l in classdiff.diff(a1, a2, enum_formatter=fn):
            print(l)

        print("-" * 40)


def changed_keys() -> None:
    @dataclass
    class A:
        a: str

    @dataclass
    class B:
        b: str

    a = {"unchanged": 1, "type_change": {"unchanged": 1, "a_or_b": A(a="a")}}
    b = {"unchanged": 1, "type_change": {"unchanged": 1, "a_or_b": B(b="b")}}

    for l in classdiff.diff(a, b):
        print(l)

    print("-" * 40)


def missing_keys() -> None:
    a = {"foo": {"x": 1, "baz": {"a": "baz-a", "b": "baz-b"}}}
    b = {"foo": {"x": 1, "biz": {"a": "biz-a", "b": "biz-b"}}}

    for l in classdiff.diff(a, b):
        print(l)

    print("-" * 40)


def with_dict() -> None:
    class Bar:
        def __init__(self, b):
            self.a = "a"
            self.b = b

    class Foo:
        def __init__(self, n, b):
            self.a = 42
            self.b = {"cat": "rat", "b": {"f": {"cat": n, "hat": True}}}
            self.c = Bar(b)

    result = classdiff.diff(Foo(43, "b"), Foo(44, "c"))
    for l in result:
        print(l)

    print("-" * 40)


def with_dataclasses() -> None:
    defined_in_code = SomeResource(
        name="my-data",
        price=2.3,
        quantity=4,
        dangerous=True,
        other=OtherClass(name="OA"),
        not_changed=OtherClass(name="Same"),
    )

    exists_in_db = SomeResource(
        name="my-data",
        price=3.3,
        quantity=4,
        dangerous=False,
        other=OtherClass(name="OB"),
        not_changed=OtherClass(name="Same"),
    )

    print("> diff(defined_in_code, None)")
    print("-" * 40)
    added = classdiff.diff(defined_in_code, None)
    for x in added:
        print(x)
    print("")

    print("> diff(defined_in_code, resource_in_db)")
    print("-" * 40)
    changed = classdiff.diff(defined_in_code, exists_in_db)
    for x in changed:
        print(x)
    print("")

    print("> diff(None, resource_in_db)")
    print("-" * 40)
    removed = classdiff.diff(None, exists_in_db)
    for x in removed:
        print(x)
    print("-" * 40)
