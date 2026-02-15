# src\file_conversor\backend\hash_backend.py

import hashlib

from enum import Enum
from pathlib import Path
from typing import Any, Callable, Sequence, override

# user-provided imports
from file_conversor.backend.abstract_backend import AbstractBackend
from file_conversor.config import Log
from file_conversor.config.locale import get_translation


# get app config
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)


class HashCheckFailed(RuntimeError):
    def __init__(self, filename: str | Path, expected: str, actual: str) -> None:
        super().__init__()
        self._filename = str(filename)
        self._expected = expected
        self._actual = actual

    @override
    def __str__(self) -> str:
        return f"'{self._filename}' - Expected: {self._expected} - Actual: {self._actual}"

    @override
    def __repr__(self) -> str:
        return f"{type(self)}({self.__str__()})"


class HashBackend(AbstractBackend):
    class SupportedInFormats(Enum):
        MD5 = "md5"
        SHA1 = "sha1"
        SHA256 = "sha256"
        SHA384 = "sha384"
        SHA512 = "sha512"
        SHA3_256 = "sha3_256"
        SHA3_384 = "sha3_384"
        SHA3_512 = "sha3_512"

    class SupportedOutFormats(Enum):
        MD5 = "md5"
        SHA1 = "sha1"
        SHA256 = "sha256"
        SHA384 = "sha384"
        SHA512 = "sha512"
        SHA3_256 = "sha3_256"
        SHA3_384 = "sha3_384"
        SHA3_512 = "sha3_512"

        @property
        def algorithm(self):
            match self:
                case HashBackend.SupportedOutFormats.MD5:
                    return hashlib.md5
                case HashBackend.SupportedOutFormats.SHA1:
                    return hashlib.sha1
                case HashBackend.SupportedOutFormats.SHA256:
                    return hashlib.sha256
                case HashBackend.SupportedOutFormats.SHA384:
                    return hashlib.sha384
                case HashBackend.SupportedOutFormats.SHA512:
                    return hashlib.sha512
                case HashBackend.SupportedOutFormats.SHA3_256:
                    return hashlib.sha3_256
                case HashBackend.SupportedOutFormats.SHA3_384:
                    return hashlib.sha3_384
                case HashBackend.SupportedOutFormats.SHA3_512:
                    return hashlib.sha3_512

    EXTERNAL_DEPENDENCIES: set[str] = set()

    def __init__(
        self,
        verbose: bool = False,
    ):
        """
        Initialize the Batch backend.
        """
        super().__init__()
        self._verbose = verbose

    def _get_hash(
            self,
            input_file: Path,
            hash_format: SupportedOutFormats,
    ):
        data = input_file.read_bytes()
        return hash_format.algorithm(data).hexdigest()

    def generate(
            self,
            input_files: Sequence[Path],
            output_file: Path,
            progress_callback: Callable[[float], Any] = lambda p: p,
    ):
        """
        Generates file hash

        :param input_files: Input files
        :param output_file: Output file
        :param progress_callback: Progress callback (0-100). Defaults to None.
        """
        res = ""
        output_file = output_file.with_suffix(output_file.suffix.lower())

        out_ext = output_file.suffix[1:]
        hash_format = HashBackend.SupportedOutFormats(out_ext)

        input_len = len(input_files)
        for idx, input_file in enumerate(input_files, start=1):
            digest = self._get_hash(input_file, hash_format)
            res += f"{digest}  {input_file.name}\n"
            progress_callback(100.0 * (float(idx) / input_len))

        output_file.write_text(res, encoding="utf-8")

    def check(
            self,
            input_file: Path,
            progress_callback: Callable[[float], Any] = lambda p: p,
    ):
        """
        Checks file hash

        :param input_files: Input files
        :param progress_callback: Progress callback (0-100). Defaults to None.

        :raises HashCheckFailed: if hash is not correct
        """
        in_ext = input_file.suffix[1:]
        hash_format = HashBackend.SupportedOutFormats(in_ext)

        lines = input_file.read_text().splitlines()
        for idx, line in enumerate(lines, start=1):
            digest, filename = line.strip().split()
            filename = input_file.parent / filename
            actual = self._get_hash(filename, hash_format)
            if actual != digest:
                logger.error(rf"'{filename}': [bold red]FAILED[/]")
                raise HashCheckFailed(filename, expected=digest, actual=actual)
            logger.info(rf"'{filename}': [bold green]OK[/]")

            progress_callback(100.0 * (float(idx) / len(lines)))


__all__ = [
    "HashBackend",
]
