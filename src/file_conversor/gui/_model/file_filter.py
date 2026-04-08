# src/file_conversor/gui/_model/file_filter.py

import re

from typing import Iterable

from file_conversor.config import LOG, get_translation


_ = get_translation()
logger = LOG.getLogger(__name__)


class FileFilter:
    def __init__(self, description: str = _('All Files'), extensions: Iterable[str] = ('.*')) -> None:
        super().__init__()
        self.description = description
        self.extensions = extensions

    def get(self) -> str:
        ext_str = " ".join(f"*.{re.sub(r"^\**\.*", "", ext).lower()}" for ext in self.extensions)
        return f"{self.description} ({ext_str})"


class FileFilters:
    def __init__(self, filters: Iterable[FileFilter] = (FileFilter(),)) -> None:
        super().__init__()
        self.filters = filters

    def get(self) -> str:
        return ";;".join(f.get() for f in self.filters)

    def get_extensions(self) -> list[str]:
        extensions: list[str] = []
        for filter in self.filters:
            extensions.extend(filter.extensions)
        logger.debug(f"FileFilter.get_extensions() = {extensions}")
        return extensions


__all__ = [
    "FileFilter",
    "FileFilters",
]
