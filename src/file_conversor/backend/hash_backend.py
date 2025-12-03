# src\file_conversor\backend\hash_backend.py

import hashlib

from typing import Any, Callable, Sequence

from pathlib import Path

from rich import print

# user-provided imports
from file_conversor.backend.abstract_backend import AbstractBackend

from file_conversor.config import Environment, Configuration, Log
from file_conversor.config.locale import get_translation

# get app config
CONFIG = Configuration.get_instance()
LOG = Log.get_instance()

_ = get_translation()
logger = LOG.getLogger(__name__)


class HashCheckFailed(RuntimeError):
    def __init__(self, filename: str | Path, expected: str, actual: str) -> None:
        super().__init__()
        self._filename = str(filename)
        self._expected = expected
        self._actual = actual

    def __str__(self) -> str:
        return f"'{self._filename}' - Expected: {self._expected} - Actual: {self._actual}"

    def __repr__(self) -> str:
        return f"{type(self)}({self.__str__()})"


class HashBackend(AbstractBackend):
    SUPPORTED_IN_FORMATS = {
        "md5": {},
        "sha1": {},
        "sha256": {},
        "sha384": {},
        "sha512": {},
        "sha3_256": {},
        "sha3_384": {},
        "sha3_512": {},
    }
    SUPPORTED_OUT_FORMATS = {
        "md5": {
            "gen_algo": hashlib.md5
        },
        "sha1": {
            "gen_algo": hashlib.sha1
        },
        "sha256": {
            "gen_algo": hashlib.sha256
        },
        "sha384": {
            "gen_algo": hashlib.sha384
        },
        "sha512": {
            "gen_algo": hashlib.sha512
        },
        "sha3_256": {
            "gen_algo": hashlib.sha3_256
        },
        "sha3_384": {
            "gen_algo": hashlib.sha3_384
        },
        "sha3_512": {
            "gen_algo": hashlib.sha3_512
        },
    }
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
            input_file: str | Path,
            algorithm: str,
    ):
        input_file = Path(input_file)
        if not input_file.exists():
            raise FileNotFoundError(f"'{input_file}' not found")
        data = input_file.read_bytes()
        algorithm_callback = self.SUPPORTED_OUT_FORMATS[algorithm]["gen_algo"]
        return algorithm_callback(data).hexdigest()

    def generate(
            self,
            input_files: Sequence[str | Path],
            output_file: str | Path,
            progress_callback: Callable[[float], Any] | None = None,
    ):
        """
        Generates file hash

        :param input_files: Input files
        :param output_file: Output file
        :param progress_callback: Progress callback (0-100). Defaults to None.
        """
        res = ""
        output_file = Path(output_file)
        output_file = output_file.with_suffix(output_file.suffix.lower())

        out_ext = output_file.suffix[1:]

        input_len = len(input_files)
        for idx, in_file in enumerate(input_files, start=1):
            input_file = Path(in_file)
            digest = self._get_hash(input_file, out_ext)
            res += f"{digest}  {input_file.name}\n"
            if progress_callback:
                progress_callback(100.0 * (float(idx) / input_len))

        output_file.write_text(res, encoding="utf-8")

    def check(
            self,
            input_file: str | Path,
            progress_callback: Callable[[float], Any] | None = None,
    ):
        """
        Checks file hash

        :param input_files: Input files
        :param progress_callback: Progress callback (0-100). Defaults to None.

        :raises HashCheckFailed: if hash is not correct
        """
        input_file = Path(input_file)
        in_ext = input_file.suffix[1:]
        if not input_file.exists():
            raise FileNotFoundError(f"'{input_file}' not found")

        lines = input_file.read_text().splitlines()
        for idx, line in enumerate(lines, start=1):
            digest, filename = line.strip().split()
            filename = input_file.parent / filename
            actual = self._get_hash(filename, in_ext)
            if actual != digest:
                logger.error(rf"'{filename}': [bold red]FAILED[/]")
                raise HashCheckFailed(filename, expected=digest, actual=actual)
            logger.info(rf"'{filename}': [bold green]OK[/]")

            progress = 100.0 * (float(idx) / len(lines))
            if progress_callback:
                progress_callback(progress)


__all__ = [
    "HashBackend",
]
