# src\file_conversor\config\dataclass_enforce_types.py

from dataclasses import fields
from types import UnionType
from typing import (
    Any, Union, Optional,
    get_origin, get_args, get_type_hints,
)


class _FieldValidator:
    def __init__(self, value: Any, expected: Any, field_name: str) -> None:
        super().__init__()
        self.value = value
        self.expected = expected
        self.field_name = field_name

        self.origin = get_origin(self.expected)
        self.args = get_args(self.expected)

    def validate(self):
        """
        Recursively validate value against expected type annotation.
        Raises TypeError if mismatched.
        """

        # Accept Any
        if self.expected is Any:
            return

        # Non-generic / base types (int, str, bool, custom classes)
        if self.origin is None:
            return self._validate_base_type()

        # Built-in generic containers (PEP 585)
        if self.origin in (Union, UnionType) or isinstance(self.expected, UnionType):
            return self._validate_union()
        if self.origin in (list, set, frozenset):
            return self._validate_iterable()
        if self.origin is tuple:
            return self._validate_tuple()
        if self.origin is dict:
            return self._validate_dict()

        # Unsupported type
        raise TypeError(
            f"Unsupported type annotation at field {self.field_name}: {self.expected!r}"
        )

    def _validate_tuple(self):
        # Check tuple type
        if not isinstance(self.value, tuple):
            raise TypeError(
                f"{self.field_name} must be tuple[...] got {self.value!r} of type {type(self.value)}"
            )

        # Homogeneous tuple: tuple[T, ...]
        if len(self.args) == 2 and self.args[1] is Ellipsis:
            (item_type,) = self.args[:1]
            for i, item in enumerate(self.value):
                _FieldValidator(value=item, expected=item_type, field_name=f"{self.field_name}[{i}]").validate()
            return

        # Heterogeneous tuple
        if len(self.args) != len(self.value):
            raise TypeError(
                f"{self.field_name} expects tuple of length {len(self.args)}, got length {len(self.value)}"
            )
        for i, (item, expected_t) in enumerate(zip(self.value, self.args)):
            _FieldValidator(value=item, expected=expected_t, field_name=f"{self.field_name}[{i}]").validate()

    def _validate_union(self):
        # Validate inner type recursively
        for t in self.args:
            try:
                _FieldValidator(value=self.value, expected=t, field_name=self.field_name).validate()
                return
            except TypeError as e:
                pass
        raise TypeError(
            f"{self.field_name} must be Union[{self.args}], got {self.value!r} of type {type(self.value)}"
        )

    def _validate_iterable(self):
        # Check list type
        expected_type = self.origin  # list, set, frozenset
        if not isinstance(self.value, expected_type):
            raise TypeError(
                f"{self.field_name} must be {expected_type}[{self.args[0]}], "
                f"got {self.value!r} of type {type(self.value)}"
            )

        # Check list item types
        (item_type,) = self.args
        for i, item in enumerate(self.value):
            try:
                _FieldValidator(value=item, expected=item_type, field_name=f"{self.field_name}[{i}]").validate()
            except TypeError as e:
                raise TypeError(f"{self.field_name} element invalid: {e}")

    def _validate_dict(self):
        # Check dict type
        if not isinstance(self.value, dict):
            raise TypeError(
                f"{self.field_name} must be dict[{self.args[0]}, {self.args[1]}], got {self.value!r} of type {type(self.value)}"
            )

        # Check dict key/value types
        key_t, val_t = self.args
        for k, v in self.value.items():
            # Validate key
            _FieldValidator(value=k, expected=key_t, field_name=f"{self.field_name}.key").validate()

            # Validate value
            _FieldValidator(value=v, expected=val_t, field_name=f"{self.field_name}[{k!r}]").validate()

    def _validate_base_type(self):
        # Special-case bool vs int: `isinstance(True, int)` is True in Python,
        # but we want strict boolean checks if expected is bool.
        if self.expected is bool:
            if not isinstance(self.value, bool):
                raise TypeError(
                    f"{self.field_name} must be bool, got {self.value!r} ({type(self.value)})"
                )
            return

        # Normal isinstance check
        print("Base value:", self.value, self.expected)
        if not isinstance(self.value, self.expected):
            raise TypeError(
                f"{self.field_name} must be {self.expected}, got {self.value!r} of type {type(self.value)}"
            )


def _validate_class(obj):
    """Validate all fields of a dataclass instance."""
    hints = get_type_hints(obj.__class__)
    for f in fields(obj):
        # Get field value and expected type, and validate
        value = getattr(obj, f.name)
        expected = hints.get(f.name, f.type)
        print("Validating field:", f.name, "value:", value, "expected:", expected)
        _FieldValidator(value, expected, f.name).validate()


def dataclass_enforce_types(cls):
    orig_post = getattr(cls, '__post_init__', None)

    def __post_init__(self):
        """Validate dataclass fields after initialization."""
        _validate_class(self)
        if orig_post:
            orig_post(self)

    cls.__post_init__ = __post_init__
    return cls


__all__ = [
    "dataclass_enforce_types",
]
