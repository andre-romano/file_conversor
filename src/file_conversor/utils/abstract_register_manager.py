# src\file_conversor\utils\abstract_register_manager.py

from dataclasses import dataclass
from typing import Any, Self


class AbstractRegisterManager:

    @dataclass
    class ConstructorDataModel:
        """ Data model to store constructor data for registered classes. """
        name: str
        args: tuple
        kwargs: dict[str, Any]

    _REGISTERED: dict[str, ConstructorDataModel] = {}
    """{name: (args, kwargs)}"""

    @classmethod
    def get_registered(cls):
        return dict(cls._REGISTERED)

    @classmethod
    def is_registered(cls, n: str) -> bool:
        return n in cls._REGISTERED

    @classmethod
    def register(cls, n: str, *args, **kwargs):
        cls._REGISTERED[n] = cls.ConstructorDataModel(name=n, args=args, kwargs=kwargs)

    @classmethod
    def from_str(cls, name: str) -> Self:
        if name not in cls._REGISTERED:
            raise ValueError(f"'{name}' not registered. Registered options: {', '.join(cls.get_registered())}")
        constructor = cls._REGISTERED[name]
        return cls(*constructor.args, **constructor.kwargs)


__all__ = [
    "AbstractRegisterManager",
]
