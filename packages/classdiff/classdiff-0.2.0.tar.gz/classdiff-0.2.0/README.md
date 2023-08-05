# `classdiff` - Python Class Difffer

This is a small library to diff (data) classes. Different from most existing
diff tools that produce data structures that show adds, removes or changes, this
tool is intended to use for printing a dataclass and higlight the diff with
different color coding, similar to the output of `Terraform` or `Pulumi`.

## Usage

Just pass your classes to the diff function to get back a representation of the
diff.

Given the following two classes:

```python
one = SomeResource(
    name="my-data",
    price=2.3,
    quantity=4,
    dangerous=True,
    other=OtherClass(name="OA"),
    not_changed=OtherClass(name="Same"),
)

two = SomeResource(
    name="my-data",
    price=3.3,
    quantity=4,
    dangerous=False,
    other=OtherClass(name="OB"),
    not_changed=OtherClass(name="Same"),
)
```

Passing them to `classdiff.diff` in combinations of `(one, None)`, `(one, two)`
and `(None, two)` and printing the lines in the returned value, the following
will be printed with colored output (green for added, red for removed and yellow
for changed). Note that each element in the returned list is of type `DiffInfo`
which implements `__repr__` to print with proper prefix and color.

```sh
> diff(one, None)
----------------------------------------
+ SomeResource(
+   dangerous = True
+   name = my-data
+   not_changed = OtherClass(
+     name = Same
+   )
+   other = OtherClass(
+     name = OA
+   )
+   price = 2.3
+   quantity = 4
+ )

> diff(one, two)
----------------------------------------
~ SomeResource(
~   dangerous = False => True
    name = my-data
    not_changed = OtherClass(
      name = Same
    )
~   other = OtherClass(
~     name = OB => OA
~   )
~   price = 3.3 => 2.3
    quantity = 4
~ )

> diff(None, two)
----------------------------------------
- SomeResource(
-   dangerous = False
-   name = my-data
-   not_changed = OtherClass(
-     name = Same
-   )
-   other = OtherClass(
-     name = OB
-   )
-   price = 3.3
-   quantity = 4
- )

```

## Development

All code is formatted and analyzed with `black` and `ruff`. Tests are run with
`pytest`.

```sh
› poetry run black .
› poetry run ruff check .
› poetry run mypy .
› poetry run pytest tests/
```
