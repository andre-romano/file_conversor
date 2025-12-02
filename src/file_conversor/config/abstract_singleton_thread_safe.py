# src/file_conversor/utils/abstract_singleton_thread_safe.py

import threading
from typing import Self


class AbstractSingletonThreadSafe:
    _instances = {}
    _lock = threading.RLock()

    @classmethod
    def get_instance(cls, *args, **kwargs) -> Self:
        with cls._lock:
            if cls not in cls._instances:
                cls._instances[cls] = cls(*args, **kwargs)
        return cls._instances[cls]


__all__ = [
    "AbstractSingletonThreadSafe",
]
