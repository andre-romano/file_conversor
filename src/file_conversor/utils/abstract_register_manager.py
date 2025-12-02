# src\file_conversor\utils\abstract_register_manager.py

from typing import Any, Self


class AbstractRegisterManager:
    _REGISTERED: dict[str, tuple[tuple, dict[str, Any]]] = {}
    """{name: (args, kwargs)}"""

    @classmethod
    def get_registered(cls):
        return dict(cls._REGISTERED)

    @classmethod
    def is_registered(cls, n: str) -> bool:
        return n in cls._REGISTERED

    @classmethod
    def register(cls, n: str, *args, **kwargs):
        cls._REGISTERED[n] = (args, kwargs)

    @classmethod
    def from_str(cls, name: str) -> Self:
        if name not in cls._REGISTERED:
            raise ValueError(f"'{name}' not registered. Registered options: {', '.join(cls.get_registered())}")
        args, kwargs = cls._REGISTERED[name]
        return cls(*args, **kwargs)


__all__ = [
    "AbstractRegisterManager",
]
