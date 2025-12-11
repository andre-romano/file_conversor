
# tests\config\test_dataclass_enforce_type.py

import platform
from typing import Optional, Union
import pytest

from dataclasses import dataclass
from pathlib import Path

# user-provided imports
from file_conversor.config import dataclass_enforce_types

from tests.utils import Test, DATA_PATH, app_cmd


# dataclass without type enforcement
@dataclass
class _DataclassNoEnforce:
    a: int
    b: str
    c: float
    d: bool


@dataclass
@dataclass_enforce_types
class _DataclassEnforce:
    a: int
    b: str
    c: float
    d: bool


@dataclass
@dataclass_enforce_types
class _DataClassWithOptional:
    a: Optional[int]
    b: Union[str, None]
    c: float | None


@dataclass
@dataclass_enforce_types
class _DataClassWithListDictTuple:
    a: list[int]
    b: dict[str, float]
    c: tuple[int, str]


class TestAbstractBackend:
    def test_dataclass(self):
        obj = _DataclassNoEnforce(a=1, b="string", c=1.5, d=True)
        assert obj.a == 1
        assert obj.b == "string"
        assert obj.c == 1.5
        assert obj.d == True

        obj = _DataclassNoEnforce(1, "string", 1.5, True)
        assert obj.a == 1
        assert obj.b == "string"
        assert obj.c == 1.5
        assert obj.d == True

    def test_dataclass_no_enforce(self):
        # wrong types but no enforcement
        obj = _DataclassNoEnforce(a="1", b=2, c="3.5", d=False)  # pyright: ignore[reportArgumentType]
        assert obj.a == "1"
        assert obj.b == 2
        assert obj.c == "3.5"
        assert obj.d == False

    def test_dataclass_enforce(self):
        obj = _DataclassEnforce(a=1, b="string", c=1.5, d=True)
        assert obj.a == 1
        assert obj.b == "string"
        assert obj.c == 1.5
        assert obj.d == True

        obj = _DataclassEnforce(1, "string", 1.5, True)
        assert obj.a == 1
        assert obj.b == "string"
        assert obj.c == 1.5
        assert obj.d == True

        with pytest.raises(TypeError):
            obj = _DataclassEnforce(a="1", b=2, c="3.5", d='false')  # pyright: ignore[reportArgumentType]

    def test_dataclass_enforce_partial_wrong(self):
        with pytest.raises(TypeError):
            obj = _DataclassEnforce(a=1, b=2, c=3.5, d=True)  # pyright: ignore[reportArgumentType]

        with pytest.raises(TypeError):
            obj = _DataclassEnforce(a="1", b="string", c=1.5, d=True)  # pyright: ignore[reportArgumentType]

    def test_dataclass_enforce_optional(self):
        obj = _DataClassWithOptional(a=None, b="test", c=5.5)
        assert obj.a is None
        assert obj.b == "test"
        assert obj.c == 5.5

        obj = _DataClassWithOptional(a=1, b=None, c=2.5)
        assert obj.a == 1
        assert obj.b is None
        assert obj.c == 2.5

        obj = _DataClassWithOptional(a=1, b="string", c=None)
        assert obj.a == 1
        assert obj.b == "string"
        assert obj.c is None

        with pytest.raises(TypeError):
            obj = _DataClassWithOptional(a='1', b=None, c=3.5)  # pyright: ignore[reportArgumentType]

        with pytest.raises(TypeError):
            obj = _DataClassWithOptional(a=None, b=2, c=None)  # pyright: ignore[reportArgumentType]

    def test_dataclass_enforce_list_dict_tuple(self):
        obj = _DataClassWithListDictTuple(a=[1, 2, 3], b={"key": 1.5}, c=(1, "str"))
        assert obj.a == [1, 2, 3]
        assert obj.b == {"key": 1.5}
        assert obj.c == (1, "str")
