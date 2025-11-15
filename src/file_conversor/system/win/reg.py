# src\file_conversor\system\win\reg.py

import json
import re

from pathlib import Path
from typing import Iterable, Self

# user-provided imports
from file_conversor.config.log import Log

LOG = Log.get_instance()

logger = LOG.getLogger(__name__)


class WinRegKey:
    KEY_RE = re.compile(r'^\[(.*?)\]$')
    VALUE_RE = re.compile(r'^(?:"([^"]+)"|@)=(?:"(.*)"|dword:[0-9a-fA-F]+|hex:[0-9a-fA-F,]+)$')

    def __init__(self, path: str) -> None:
        r"""Initializes RegKey with path of type HKEY_*\\* """
        super().__init__()
        self._data: dict[str, str] = {}
        self.path = path

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, p):
        self._path = p

    def __eq__(self, other):
        return isinstance(other, WinRegKey) and self.path == other.path

    def __hash__(self):
        return hash(self.path)

    def __str__(self) -> str:
        return self.path

    def __repr__(self) -> str:
        res = [f"[{self._path}]"]
        for name, content in self._data.items():
            name_str = json.dumps(name) if name and name != "@" else "@"
            content_str = json.dumps(content) if content else '""'
            res.append(f'{name_str}={content_str}')
        return "\n".join(res)

    def __contains__(self, name: str):
        return name in self._data

    def __getitem__(self, name: str):
        return self._data[name]

    def items(self):
        return self._data.items()

    def add_value(self, name: str, content: str | int | bytes) -> Self:
        """
        Add value to windows key

        :param name: value name
        :param content: value content.

        :raises TypeError: content type is invalid
        """
        name_str = "@" if not name else name

        content_str = ""
        if isinstance(content, str):
            content_str = content
        elif isinstance(content, int):
            content_str = f"dword:{content:08x}"  # Pad to 8 digits
        elif isinstance(content, bytes):
            content_str = f"hex:{content.hex()}"
        else:
            raise TypeError(f"Content '{content}' type is not str|int.")

        self._data[name_str] = content_str
        # logger.debug(f'Add value "{name_str}={content_str}"')
        return self

    def del_value(self, name: str) -> Self:
        if name in self._data:
            del self._data[name]
            # logger.debug(f'Del value "{name}"')
        return self

    def update(self, key: Self | dict[str, str | int | bytes]) -> Self:
        if isinstance(key, WinRegKey):
            self._data.update(key._data)
        else:
            for name, content in key.items():
                self.add_value(name, content)
        # logger.info(f'Updated reg key {self.path}')
        return self


class WinRegFile:
    def __init__(self, input_path_or_winregfile: str | Path | Self | None = None) -> None:
        """
        Initialized WinRegFile

        :param input_path_or_winregfile: .REG file or WinRegFile. Defaults to None (do not load file).
        """
        super().__init__()
        self._data: dict[str, WinRegKey] = {}

        if isinstance(input_path_or_winregfile, (str, Path)):
            self.load(input_path_or_winregfile)
        elif isinstance(input_path_or_winregfile, WinRegFile):
            self.update(input_path_or_winregfile)

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        res = ["Windows Registry Editor Version 5.00"]
        for name, key in self._data.items():
            res.append(repr(key))
        return "\n\n".join(res)

    def __iter__(self):
        return self._data.__iter__()

    def __getitem__(self, key: str | WinRegKey):
        if isinstance(key, str):
            return self._data[key]
        elif isinstance(key, WinRegKey):
            return self._data[key.path]
        else:
            raise KeyError("Key search supports only str|WinRegKey")

    def items(self):
        return self._data.items()

    def add_key(self, key: WinRegKey) -> Self:
        if key.path in self._data:
            key_current = self._data[key.path]
            for name, value in key.items():
                key_current.add_value(name, value)
        else:
            self._data[key.path] = key
        # logger.debug(f"Add key '{key.path}'")
        return self

    def del_key(self, key: WinRegKey) -> Self:
        if key.path in self._data:
            del self._data[key.path]
            # logger.debug(f"Delete key '{key.path}'")
        return self

    def update(self, reg: Self | Iterable[WinRegKey]) -> Self:
        if isinstance(reg, WinRegFile):
            for _, key in reg.items():
                self.add_key(key)
        else:
            for key in reg:
                self.add_key(key)
        # logger.info(f"Updated reg file")
        return self

    def dump(self, output_file: str | Path):
        """
        Dump WinRegFile into .REG file.

        :param output_file: Output .REG file.     
        """
        out_file = f"{str(output_file).replace(".reg", "")}.reg"
        with open(out_file, "wb") as f:
            f.write(b'\xff\xfe')     # BOM
            f.write(repr(self).encode("utf-16le"))
        logger.info(f"Dumped reg file into '{output_file}'")

    def dumps(self) -> str:
        """
        Dumps WinRegFile into string.
        """
        return repr(self)

    def load(self, input_path: str | Path):
        """
        Loads a .REG file into WinRegFile

        :param input_path: Input .REG file

        :raises FileNotFoundError: Input file not exists.
        :raises RuntimeError: Invalid REG format. Value not associated with key.
        """
        input_path = Path(input_path)
        if not input_path.exists():
            raise FileNotFoundError(f"Input file '{input_path}' not exists")
        input_text = input_path.read_text(encoding="utf-16")
        if not input_text.startswith("Windows Registry Editor Version 5.00"):
            raise RuntimeError("Invalid .REG format")

        reg_key: WinRegKey | None = None
        for line in input_text.splitlines():
            match_key = re.match(WinRegKey.KEY_RE, line)
            if match_key:
                reg_key = WinRegKey(match_key.group(1))
                self.add_key(reg_key)
                continue

            match_value = re.match(WinRegKey.VALUE_RE, line)
            if match_value:
                name = match_value.group(1) or "@"
                content = match_value.group(2)

                if content.startswith("dword:"):
                    content = int(content.replace("dword:", ""), 16)
                elif content.startswith("hex:"):
                    hex_str = content.replace("hex:", "").replace(",", "")
                    content = bytes.fromhex(hex_str)
                if not reg_key:
                    raise RuntimeError(f"Invalid reg file. Value '{name}' not associated with a key.")
                reg_key.add_value(name, content)

        logger.info(f"Input file '{input_path}' loaded")


__all__ = [
    "WinRegFile",
    "WinRegKey",
]
